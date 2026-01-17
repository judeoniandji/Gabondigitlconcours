from django.db import models
from django.conf import settings

class Notification(models.Model):
    destinataire = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    type = models.CharField(max_length=10, choices=[('mail', 'Mail'), ('sms', 'SMS'), ('system', 'Système')])
    contenu = models.TextField()
    date_envoi = models.DateTimeField(auto_now_add=True)
    statut = models.CharField(max_length=20, default='en_attente')  # en_attente, envoye, erreur
    lu = models.BooleanField(default=False)

class Message(models.Model):
    expediteur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='messages_envoyes')
    destinataire = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='messages_recus')
    sujet = models.CharField(max_length=255)
    contenu = models.TextField()
    date_envoi = models.DateTimeField(auto_now_add=True)
    lu = models.BooleanField(default=False)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='reponses')

    class Meta:
        ordering = ['-date_envoi']
