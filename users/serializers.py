from rest_framework import serializers
from .models import User, Candidat, Gestionnaire

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'telephone']

class CandidatSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Candidat
        fields = ['id', 'user', 'date_naissance', 'lieu_naissance', 'adresse', 'document_identite']

class GestionnaireSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Gestionnaire
        fields = ['id', 'user', 'fonction']
