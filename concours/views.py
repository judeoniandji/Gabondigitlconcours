from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.db.models import Sum, F, ExpressionWrapper, FloatField
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
        coeff_sum = serie.matieres.aggregate(total=Sum('coefficient'))['total'] or 1.0

        # This query calculates the weighted score for each candidate at the database level.
        # It annotates each candidate with a 'score' by summing the product of note value and matiere coefficient.
        # This is significantly more efficient than fetching all notes and processing them in Python.
        notes = Note.objects.filter(matiere__serie=serie, etat='valide') \
            .values('candidat__numero_candidat') \
            .annotate(score=Sum(F('valeur') * F('matiere__coefficient'))) \
            .order_by('-score')

        # The calculated score is then used to determine the average,
        # which is wrapped in an ExpressionWrapper to specify the output field type.
        # This avoids potential precision issues with DecimalField in aggregations.
        classement = notes.annotate(
            moyenne=ExpressionWrapper(
                F('score') / float(coeff_sum),
                output_field=FloatField()
            )
        ).values('candidat__numero_candidat', 'moyenne')

        # The resulting classement is a list of dictionaries, ready for the response.
        # The ordering is handled by the database, making the sort in Python redundant.
        classement_list = [
            {'numero_candidat': item['candidat__numero_candidat'], 'moyenne': round(item['moyenne'], 2)}
            for item in classement
        ]

        return Response({'serie': serie.id, 'classement': classement_list})

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
