from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.conf import settings

class User(AbstractUser):
    ROLE_CHOICES = [
        ('candidat', 'Candidat'),
        ('gestionnaire', 'Gestionnaire'),
        ('jury', 'Jury'),
        ('secretaire', 'Secrétaire'),
        ('correcteur', 'Correcteur'),
        ('president_jury', 'Président de jury'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    token_valid_after = models.DateTimeField(default=timezone.now)
    telephone = models.CharField(max_length=20, blank=True)
    # Ajout d'autres champs communs si besoin

class Candidat(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='candidat_profile')
    nom_complet = models.CharField(max_length=255, blank=True)
    date_naissance = models.DateField(null=True, blank=True)
    lieu_naissance = models.CharField(max_length=100, blank=True)
    ville_naissance = models.CharField(max_length=100, blank=True)
    adresse = models.CharField(max_length=255, blank=True)
    document_identite = models.FileField(upload_to='documents/', blank=True)
    historique_academique = models.TextField(blank=True, help_text="Détails du parcours académique")
    numero_candidat = models.CharField(max_length=20, unique=True, null=True, blank=True)
    # Ajout d'autres champs spécifiques au candidat

class Gestionnaire(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='gestionnaire_profile')
    fonction = models.CharField(max_length=50, blank=True)
    # Ajout d'autres champs spécifiques au gestionnaire

class AuditLog(models.Model):
    acteur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    action = models.CharField(max_length=100)
    ressource = models.CharField(max_length=100)
    ressource_id = models.IntegerField(null=True, blank=True)
    payload = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class BugReport(models.Model):
    SEVERITY_CHOICES = [
        ('bloquant', 'Bloquant'),
        ('majeur', 'Majeur'),
        ('mineur', 'Mineur'),
        ('cosmetique', 'Cosmétique'),
    ]
    STATUS_CHOICES = [
        ('ouvert', 'Ouvert'),
        ('en_cours', 'En cours'),
        ('corrige', 'Corrigé'),
        ('valide', 'Validé'),
        ('rejete', 'Rejeté'),
    ]
    titre = models.CharField(max_length=200)
    description = models.TextField()
    etapes = models.TextField(blank=True)
    environnement = models.CharField(max_length=200, blank=True)
    severite = models.CharField(max_length=20, choices=SEVERITY_CHOICES, default='mineur')
    statut = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ouvert')
    module = models.CharField(max_length=100, blank=True)
    chemins = models.TextField(blank=True)
    reporter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='reported_bugs')
    assigne = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_bugs')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class BugEvent(models.Model):
    bug = models.ForeignKey(BugReport, on_delete=models.CASCADE, related_name='events')
    type = models.CharField(max_length=50)
    detail = models.TextField(blank=True)
    auteur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
