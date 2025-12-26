from django.db import models

class Paiement(models.Model):
    candidat = models.ForeignKey('users.Candidat', on_delete=models.CASCADE)
    concours = models.ForeignKey('concours.Concours', on_delete=models.CASCADE)
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    date_paiement = models.DateTimeField(auto_now_add=True)
    reference = models.CharField(max_length=100, unique=True)
    statut = models.CharField(max_length=20, default='en_attente')  # en_attente, valide, rejete
