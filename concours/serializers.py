from rest_framework import serializers
from .models import Concours, Dossier, Resultat
from .models import Serie, Matiere, Note
from users.models import Candidat

class ConcoursSerializer(serializers.ModelSerializer):
    documents_requis_list = serializers.SerializerMethodField()
    limite_age_display = serializers.SerializerMethodField()
    
    class Meta:
        model = Concours
        fields = '__all__'
    
    def get_documents_requis_list(self, obj):
        """Retourne la liste des documents requis sous forme de liste"""
        return obj.get_documents_requis_list()
    
    def get_limite_age_display(self, obj):
        """Retourne l'affichage formaté de la limite d'âge"""
        return obj.get_limite_age_display()

class DossierSerializer(serializers.ModelSerializer):
    candidat_numero = serializers.SerializerMethodField()
    class Meta:
        model = Dossier
        fields = '__all__'
        extra_fields = ['candidat_numero']

    def get_candidat_numero(self, obj):
        try:
            return getattr(obj.candidat, 'numero_candidat', None)
        except Exception:
            return None

class ResultatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resultat
        fields = '__all__'

class SerieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Serie
        fields = '__all__'

class MatiereSerializer(serializers.ModelSerializer):
    class Meta:
        model = Matiere
        fields = '__all__'

class NoteSerializer(serializers.ModelSerializer):
    candidat_numero = serializers.CharField(source='candidat.numero_candidat', read_only=True)
    candidat_numero_input = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Note
        fields = ['id', 'matiere', 'valeur', 'etat', 'saisi_par', 'valide_par', 'date_saisie', 'date_validation', 'candidat_numero', 'candidat_numero_input']
        read_only_fields = ['saisi_par', 'valide_par', 'date_saisie', 'date_validation', 'etat']

    def create(self, validated_data):
        num = validated_data.pop('candidat_numero_input', None)
        if num:
            try:
                candidat = Candidat.objects.get(numero_candidat=num)
                validated_data['candidat'] = candidat
            except Candidat.DoesNotExist:
                raise serializers.ValidationError({"candidat_numero_input": "Candidat introuvable"})
        return super().create(validated_data)

