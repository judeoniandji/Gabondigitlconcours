from rest_framework import serializers
from .models import Concours, Dossier, Resultat
from .models import Serie, Matiere, Note

class ConcoursSerializer(serializers.ModelSerializer):
    class Meta:
        model = Concours
        fields = '__all__'

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
    class Meta:
        model = Note
        fields = '__all__'
