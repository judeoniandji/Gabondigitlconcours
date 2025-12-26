from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = [
        ('candidat', 'Candidat'),
        ('gestionnaire', 'Gestionnaire'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    telephone = models.CharField(max_length=20, blank=True)
    # Ajout d'autres champs communs si besoin

class Candidat(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='candidat_profile')
    date_naissance = models.DateField(null=True, blank=True)
    lieu_naissance = models.CharField(max_length=100, blank=True)
    adresse = models.CharField(max_length=255, blank=True)
    document_identite = models.FileField(upload_to='documents/', blank=True)
    # Ajout d'autres champs spécifiques au candidat

class Gestionnaire(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='gestionnaire_profile')
    fonction = models.CharField(max_length=50, blank=True)
    # Ajout d'autres champs spécifiques au gestionnaire
