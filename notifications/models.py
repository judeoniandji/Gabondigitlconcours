from django.db import models

class Notification(models.Model):
    destinataire = models.ForeignKey('users.User', on_delete=models.CASCADE)
    type = models.CharField(max_length=10, choices=[('mail', 'Mail'), ('sms', 'SMS')])
    contenu = models.TextField()
    date_envoi = models.DateTimeField(auto_now_add=True)
    statut = models.CharField(max_length=20, default='en_attente')  # en_attente, envoye, erreur
