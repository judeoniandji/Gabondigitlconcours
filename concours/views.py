from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.db import models
from django.db.models import Sum, F, Prefetch
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
        matieres = list(serie.matieres.all())
        coeff_sum = sum([float(m.coefficient) for m in matieres]) or 1.0
        # notes validées par candidat
        notes = Note.objects.filter(matiere__serie=serie, etat='valide')
        # regroupement par candidat
        scores = {}
        for n in notes.select_related('matiere', 'candidat'):
            num = getattr(n.candidat, 'numero_candidat', n.candidat_id)
            scores.setdefault(num, 0.0)
            scores[num] += float(n.valeur) * float(n.matiere.coefficient)
        classement = [{'numero_candidat': k, 'moyenne': round(v/coeff_sum, 2)} for k, v in scores.items()]
        classement.sort(key=lambda x: x['moyenne'], reverse=True)
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
        # Optimization: Resolve N+1 query on notes.
        # Prefetch all notes for the given matiere and related candidats.
        # This reduces the query count from N+1 to 2.
        dossiers = Dossier.objects.filter(
            serie=matiere.serie, statut='valide'
        ).select_related('candidat').prefetch_related(
            Prefetch(
                'candidat__note_set',
                queryset=Note.objects.filter(matiere=matiere),
                to_attr='notes_for_matiere'
            )
        )

        data = []
        for d in dossiers:
            # Use the prefetched note if it exists
            note = d.candidat.notes_for_matiere[0] if hasattr(d.candidat, 'notes_for_matiere') and d.candidat.notes_for_matiere else None
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
