from django.shortcuts import render

from rest_framework import viewsets
from .models import User, Candidat, Gestionnaire
from .serializers import UserSerializer, CandidatSerializer, GestionnaireSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class CandidatViewSet(viewsets.ModelViewSet):
    queryset = Candidat.objects.all()
    serializer_class = CandidatSerializer

class GestionnaireViewSet(viewsets.ModelViewSet):
    queryset = Gestionnaire.objects.all()
    serializer_class = GestionnaireSerializer
