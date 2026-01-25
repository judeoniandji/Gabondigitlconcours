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
        serie = self.get_object()

        # Optimisation: Calcul de la somme des coefficients en une seule requête
        coeff_sum_result = serie.matieres.aggregate(total=Sum('coefficient'))
        coeff_sum = coeff_sum_result['total']

        if not coeff_sum:
            return Response({'serie': serie.id, 'classement': []})

        # Optimisation: Agréger les scores directement en base de données pour éviter de charger toutes les notes en mémoire
        # Cela résout le problème N+1 et est beaucoup plus performant
        scores_query = Note.objects.filter(
            matiere__serie=serie,
            etat='valide'
        ).values(
            'candidat_id', 'candidat__numero_candidat'
        ).annotate(
            total_points=Sum(F('valeur') * F('matiere__coefficient'))
        ).order_by('-total_points')

        # Formattage du classement
        classement = [
            {
                'numero_candidat': item['candidat__numero_candidat'] or f"ID_{item['candidat_id']}",
                'moyenne': round(float(item['total_points']) / float(coeff_sum), 2)
            }
            for item in scores_query
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
