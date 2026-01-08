from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.db.models import Sum, F, FloatField, CharField
from django.db.models.functions import Cast, Coalesce, Round
from django.db.models.query import QuerySet
from django.utils import timezone
from .models import Concours, Dossier, Resultat, Serie, Matiere, Note
from .serializers import ConcoursSerializer, DossierSerializer, ResultatSerializer, SerieSerializer, MatiereSerializer, NoteSerializer
from users.permissions import IsGestionnaireOrAdmin, IsCorrecteur, IsPresidentJury, IsSecretaireOrAdmin, IsCandidat
from users.models import AuditLog

class ConcoursViewSet(viewsets.ModelViewSet):
    queryset: QuerySet[Concours] = Concours.objects.all()
    serializer_class = ConcoursSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        qs = super().get_queryset()
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
        matieres = serie.matieres.all()
        coeff_sum = matieres.aggregate(total=Sum('coefficient', output_field=FloatField()))['total'] or 1.0

        # This performs the entire calculation in the database, which is much more efficient.
        # It groups notes by candidate, calculates the weighted score, and then the average.
        classement = Note.objects.filter(
            matiere__serie=serie,
            etat='valide'
        ).values(
            'candidat'
        ).annotate(
            numero_candidat=Coalesce(
                'candidat__numero_candidat',
                Cast('candidat_id', CharField())
            ),
            total_points=Sum(F('valeur') * F('matiere__coefficient'), output_field=FloatField())
        ).annotate(
            moyenne=Round(F('total_points') / coeff_sum, 2)
        ).order_by(
            '-moyenne'
        ).values(
            'numero_candidat', 'moyenne'
        )

        return Response({'serie': serie.id, 'classement': list(classement)})

class MatiereViewSet(viewsets.ModelViewSet):
    queryset: QuerySet[Matiere] = Matiere.objects.all()
    serializer_class = MatiereSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsGestionnaireOrAdmin()]
        return super().get_permissions()

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
