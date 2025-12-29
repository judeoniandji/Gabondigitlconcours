from django.db import models

class Concours(models.Model):
    nom = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    date_ouverture = models.DateField()
    date_fermeture = models.DateField()
    frais_inscription = models.DecimalField(max_digits=10, decimal_places=2)
    publie = models.BooleanField(default=False)
    # Ajout d'autres champs spécifiques au concours

class Dossier(models.Model):
    candidat = models.ForeignKey('users.Candidat', on_delete=models.CASCADE)
    concours = models.ForeignKey('Concours', on_delete=models.CASCADE)
    date_soumission = models.DateTimeField(auto_now_add=True)
    statut = models.CharField(max_length=20, default='en_attente')  # en_attente, valide, rejete
    justificatif = models.FileField(upload_to='justificatifs/', blank=True)
    reference = models.CharField(max_length=100, unique=True, null=True, blank=True)

class Resultat(models.Model):
    dossier = models.OneToOneField(Dossier, on_delete=models.CASCADE)
    note = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    admis = models.BooleanField(default=False)
    date_publication = models.DateTimeField(auto_now_add=True)

class Serie(models.Model):
    nom = models.CharField(max_length=100)
    concours = models.ForeignKey(Concours, on_delete=models.CASCADE, related_name='series')

class Matiere(models.Model):
    nom = models.CharField(max_length=100)
    coefficient = models.DecimalField(max_digits=5, decimal_places=2)
    serie = models.ForeignKey(Serie, on_delete=models.CASCADE, related_name='matieres')

class Note(models.Model):
    ETAT_CHOICES = [('brouillon', 'Brouillon'), ('valide', 'Valide')]
    candidat = models.ForeignKey('users.Candidat', on_delete=models.CASCADE)
    matiere = models.ForeignKey(Matiere, on_delete=models.CASCADE)
    valeur = models.DecimalField(max_digits=5, decimal_places=2)
    etat = models.CharField(max_length=10, choices=ETAT_CHOICES, default='brouillon')
    saisi_par = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True, related_name='notes_saisies')
    valide_par = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='notes_validees')
    date_saisie = models.DateTimeField(auto_now_add=True)
    date_validation = models.DateTimeField(null=True, blank=True)
