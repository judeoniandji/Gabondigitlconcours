from rest_framework import serializers
from .models import Notification, Message
from users.serializers import UserSerializer

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'

class MessageSerializer(serializers.ModelSerializer):
    expediteur = UserSerializer(read_only=True)
    expediteur_id = serializers.IntegerField(write_only=True, required=False)
    destinataire = UserSerializer(read_only=True)
    destinataire_id = serializers.IntegerField(write_only=True)
    reponses = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = ['id', 'expediteur', 'expediteur_id', 'destinataire', 'destinataire_id', 'sujet', 'contenu', 'date_envoi', 'lu', 'parent', 'reponses']
        read_only_fields = ['expediteur', 'date_envoi']

    def get_reponses(self, obj):
        reponses = obj.reponses.all()
        return MessageSerializer(reponses, many=True).data

    def create(self, validated_data):
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            validated_data['expediteur'] = request.user
        return super().create(validated_data)
