from django.shortcuts import render

from rest_framework import viewsets
from .models import Concours, Dossier, Resultat
from .serializers import ConcoursSerializer, DossierSerializer, ResultatSerializer

class ConcoursViewSet(viewsets.ModelViewSet):
    queryset = Concours.objects.all()
    serializer_class = ConcoursSerializer

class DossierViewSet(viewsets.ModelViewSet):
    queryset = Dossier.objects.all()
    serializer_class = DossierSerializer

class ResultatViewSet(viewsets.ModelViewSet):
    queryset = Resultat.objects.all()
    serializer_class = ResultatSerializer
