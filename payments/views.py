from django.shortcuts import render

from rest_framework import viewsets
from .models import Paiement
from .serializers import PaiementSerializer

class PaiementViewSet(viewsets.ModelViewSet):
    queryset = Paiement.objects.all()
    serializer_class = PaiementSerializer
