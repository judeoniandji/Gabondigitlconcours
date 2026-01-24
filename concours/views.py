from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.db.models import Sum, F, FloatField, ExpressionWrapper
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

        # Le calcul est maintenant entièrement fait en base de données pour une meilleure performance.
        # On annote chaque candidat avec son score total pondéré et la somme des coefficients.
        # la division se fait en flottants pour préserver la précision.
        #
        # Voici les étapes de l'optimisation :
        # 1. `serie.matieres.aggregate(total_coeff=Sum('coefficient'))`: Calcule la somme totale des coefficients pour la série.
        # 2. `Note.objects.filter(matiere__serie=serie, etat='valide')`: Filtre les notes validées pour la série.
        # 3. `.values('candidat__numero_candidat')`: Regroupe les notes par candidat.
        # 4. `.annotate(total_points=Sum(F('valeur') * F('matiere__coefficient')))`: Calcule le total des points pondérés pour chaque candidat.
        # 5. `total_coeff = serie.matieres.aggregate(total_coeff=Sum('coefficient'))['total_coeff'] or 1.0`: Récupère la somme des coefficients.
        # 6. `moyenne = F('total_points') / float(total_coeff)`: Calcule la moyenne.
        # 7. `.order_by('-moyenne')`: Ordonne les résultats par moyenne décroissante.

        total_coeff = serie.matieres.aggregate(total_coeff=Sum('coefficient'))['total_coeff'] or 1.0

        classement_qs = Note.objects.filter(matiere__serie=serie, etat='valide') \
            .values('candidat__numero_candidat') \
            .annotate(
                total_points=Sum(F('valeur') * F('matiere__coefficient'))
            ) \
            .annotate(
                moyenne=ExpressionWrapper(
                    F('total_points') / float(total_coeff),
                    output_field=FloatField()
                )
            ) \
            .order_by('-moyenne')

        # Formatage du résultat final
        classement = [
            {
                'numero_candidat': item['candidat__numero_candidat'],
                'moyenne': round(item['moyenne'], 2)
            }
            for item in classement_qs
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
