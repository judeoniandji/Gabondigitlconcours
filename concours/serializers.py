from rest_framework import serializers
from .models import Concours, Dossier, Resultat

class ConcoursSerializer(serializers.ModelSerializer):
    class Meta:
        model = Concours
        fields = '__all__'

class DossierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dossier
        fields = '__all__'

class ResultatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resultat
        fields = '__all__'
