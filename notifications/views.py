from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from .models import Notification, Message
from .serializers import NotificationSerializer, MessageSerializer

class NotificationViewSet(viewsets.ModelViewSet):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(destinataire=self.request.user)

    @action(detail=True, methods=['post'])
    def marquer_lu(self, request, pk=None):
        notification = self.get_object()
        notification.lu = True
        notification.save()
        return Response({'status': 'ok'})

class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        # Messages envoyés ou reçus par l'utilisateur, qui sont des fils principaux (pas de parent)
        # Les réponses sont chargées via le serializer
        return Message.objects.filter(
            (Q(expediteur=user) | Q(destinataire=user)) & Q(parent__isnull=True)
        ).distinct()

    def perform_create(self, serializer):
        serializer.save(expediteur=self.request.user)

    @action(detail=True, methods=['post'])
    def repondre(self, request, pk=None):
        parent = self.get_object()
        contenu = request.data.get('contenu')
        if not contenu:
            return Response({'error': 'Contenu requis'}, status=400)
        
        # Le destinataire est l'autre partie
        destinataire = parent.expediteur if parent.destinataire == request.user else parent.destinataire
        
        reponse = Message.objects.create(
            expediteur=request.user,
            destinataire=destinataire,
            sujet=f"Re: {parent.sujet}",
            contenu=contenu,
            parent=parent
        )
        return Response(MessageSerializer(reponse).data)
