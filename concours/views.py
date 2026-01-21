from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.db.models import Sum, F
from django.db.models.query import QuerySet
from django.utils import timezone
from .models import Concours, Dossier, Resultat, Serie, Matiere, Note
from .serializers import ConcoursSerializer, DossierSerializer, ResultatSerializer, SerieSerializer, MatiereSerializer, NoteSerializer
from users.permissions import IsGestionnaireOrAdmin, IsCorrecteur, IsPresidentJury, IsSecretaireOrAdmin, IsCandidat, IsCorrecteurOrAdmin
from users.models import AuditLog

class ConcoursViewSet(viewsets.ModelViewSet):
    queryset: QuerySet[Concours] = Concours.objects.all()
    serializer_class = ConcoursSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user

        if user.is_authenticated and not user.is_superuser:
            if user.role in ['gestionnaire', 'admin']:
                qs = qs.filter(admins=user)
        
        ouvert = self.request.query_params.get('ouvert')
        if ouvert == 'true':
            from django.utils import timezone as tz
            today = tz.now().date()
            qs = qs.filter(date_ouverture__lte=today, date_fermeture__gte=today)
        return qs

    @action(detail=True, methods=['put'])
    def publier(self, request, pk=None):
        concours = self.get_object()
        concours.publie = True
        concours.save(update_fields=['publie'])
        try:
            AuditLog._default_manager.create(acteur=request.user, action='concours_publier', ressource='concours', ressource_id=concours.id)
        except Exception:
            pass
        return Response({'detail': 'Résultats publiés'})

class DossierViewSet(viewsets.ModelViewSet):
    queryset: QuerySet[Dossier] = Dossier.objects.all()
    serializer_class = DossierSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        
        if user.is_authenticated:
            if user.role == 'candidat' and hasattr(user, 'candidat_profile'):
                qs = qs.filter(candidat=user.candidat_profile)
            elif user.role in ['gestionnaire', 'admin'] and not user.is_superuser:
                qs = qs.filter(concours__admins=user)

        ref = self.request.query_params.get('reference')
        cid = self.request.query_params.get('candidat_id')
        if ref:
            qs = qs.filter(reference=ref)
        if cid:
            qs = qs.filter(candidat_id=cid)
        return qs

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsSecretaireOrAdmin()]
        if self.action == 'create':
            return [IsCandidat()]
        return super().get_permissions()

    def perform_update(self, serializer):
        instance = serializer.save()
        if instance.statut == 'valide' and not instance.candidat.numero_candidat:
            import random
            import string
            from users.models import Candidat
            prefix = 'C' + timezone.now().strftime('%y')
            while True:
                suffix = ''.join(random.choices(string.digits, k=6))
                num = f"{prefix}-{suffix}"
                if not Candidat.objects.filter(numero_candidat=num).exists():
                    instance.candidat.numero_candidat = num
                    instance.candidat.save(update_fields=['numero_candidat'])
                    break
    

class ResultatViewSet(viewsets.ModelViewSet):
    queryset: QuerySet[Resultat] = Resultat.objects.all()
    serializer_class = ResultatSerializer

class SerieViewSet(viewsets.ModelViewSet):
    queryset: QuerySet[Serie] = Serie.objects.all()
    serializer_class = SerieSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsGestionnaireOrAdmin()]
        return super().get_permissions()

    @action(detail=True, methods=['get'])
    def classement(self, request, pk=None):
        """
        ⚡ Bolt: Optimized classement generation.
        - Replaced inefficient in-memory Python loops with a single, efficient database query.
        - Uses Django ORM's `annotate` and `aggregate` to perform calculations in the database.
        - Expected Impact: Reduces query count from N+1 to 2, significantly faster for large datasets.
        """
        serie = self.get_object()

        # 1. Calculate the total coefficient sum for the series.
        coeff_sum_result = serie.matieres.aggregate(total=Sum('coefficient'))
        coeff_sum = coeff_sum_result['total']
        if not coeff_sum:
            return Response({'serie': serie.id, 'classement': []})

        # 2. Calculate candidate rankings in a single, annotated query.
        from django.db.models import FloatField, CharField
        from django.db.models.functions import Cast, Coalesce
        # This groups notes by candidate, calculates the weighted score, and computes the average.
        # Coalesce is used to fall back to the candidate's ID if numero_candidat is not set.
        classement_data = Note.objects.filter(
            matiere__serie=serie, etat='valide'
        ).values(
            'candidat'  # Group by candidate ID
        ).annotate(
            numero_candidat=Coalesce('candidat__numero_candidat', Cast('candidat_id', CharField())),
            total_points=Sum(F('valeur') * F('matiere__coefficient'), output_field=FloatField()),
        ).annotate(
            moyenne=(F('total_points') / float(coeff_sum))
        ).order_by(
            '-moyenne'
        ).values(
            'numero_candidat', 'moyenne'
        )

        # 3. Format the final output with rounding.
        classement = [
            {'numero_candidat': item['numero_candidat'], 'moyenne': round(item['moyenne'], 2)}
            for item in classement_data
        ]

        return Response({'serie': serie.id, 'classement': classement})

class MatiereViewSet(viewsets.ModelViewSet):
    queryset: QuerySet[Matiere] = Matiere.objects.all()
    serializer_class = MatiereSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsGestionnaireOrAdmin()]
        if self.action == 'candidats':
            return [IsCorrecteurOrAdmin()]
        return super().get_permissions()

    @action(detail=True, methods=['get'])
    def candidats(self, request, pk=None):
        matiere = self.get_object()
        dossiers = Dossier.objects.filter(serie=matiere.serie, statut='valide').select_related('candidat')
        data = []
        for d in dossiers:
            note = Note.objects.filter(candidat=d.candidat, matiere=matiere).first()
            data.append({
                'dossier_id': d.id,
                'candidat_numero': getattr(d.candidat, 'numero_candidat', 'Unknown'),
                'note': NoteSerializer(note).data if note else None
            })
        return Response(data)

class NoteViewSet(viewsets.ModelViewSet):
    queryset: QuerySet[Note] = Note.objects.all()
    serializer_class = NoteSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsCorrecteur()]
        if self.action == 'valider':
            return [IsPresidentJury()]
        return super().get_permissions()

    @action(detail=True, methods=['put'])
    def valider(self, request, pk=None):
        note = self.get_object()
        note.etat = 'valide'
        note.valide_par = request.user
        note.date_validation = timezone.now()
        note.save(update_fields=['etat', 'valide_par', 'date_validation'])
        try:
            AuditLog._default_manager.create(acteur=request.user, action='note_valider', ressource='note', ressource_id=note.id, payload={'candidat': note.candidat_id, 'matiere': note.matiere_id})
        except Exception:
            pass
        return Response({'detail': 'Note validée'})
