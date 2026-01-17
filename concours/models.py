from django.db import models

class Concours(models.Model):
    NIVEAU_CHOICES = [
        ('BEPC', 'BEPC'),
        ('Bac', 'Bac'),
        ('Bac+1', 'Bac+1'),
        ('Bac+2', 'Bac+2'),
        ('Bac+3', 'Bac+3'),
        ('Bac+4', 'Bac+4'),
        ('Bac+5', 'Bac+5'),
        ('Bac+6', 'Bac+6 et plus'),
    ]
    
    nom = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    ministere_organisateur = models.CharField(max_length=200, blank=True, help_text="Ministère organisateur du concours")
    niveau_demande = models.CharField(max_length=20, choices=NIVEAU_CHOICES, blank=True, help_text="Niveau académique minimum requis")
    limite_age_min = models.IntegerField(null=True, blank=True, help_text="Âge minimum requis (années)")
    limite_age_max = models.IntegerField(null=True, blank=True, help_text="Âge maximum requis (années)")
    nombre_places = models.IntegerField(null=True, blank=True, help_text="Nombre de places disponibles")
    date_ouverture = models.DateField()
    date_fermeture = models.DateField()
    lieu_depot = models.TextField(blank=True, help_text="Adresse complète du lieu de dépôt des dossiers")
    frais_inscription = models.DecimalField(max_digits=10, decimal_places=2)
    publie = models.BooleanField(default=False)
    admins = models.ManyToManyField('users.User', related_name='concours_administres', blank=True, limit_choices_to={'role__in': ['gestionnaire', 'admin']})
    
    # Documents requis (stockés comme texte séparé par des virgules, format: "doc1,doc2,doc3")
    documents_requis = models.TextField(blank=True, help_text="Liste des documents requis (séparés par des virgules)")
    
    def get_documents_requis_list(self):
        """Retourne la liste des documents requis sous forme de liste Python"""
        if not self.documents_requis:
            return []
        return [doc.strip() for doc in self.documents_requis.split(',') if doc.strip()]
    
    def get_limite_age_display(self):
        """Retourne un affichage formaté de la limite d'âge"""
        if self.limite_age_min and self.limite_age_max:
            return f"{self.limite_age_min} - {self.limite_age_max} ans"
        elif self.limite_age_min:
            return f"Minimum {self.limite_age_min} ans"
        elif self.limite_age_max:
            return f"Maximum {self.limite_age_max} ans"
        return None

class Dossier(models.Model):
    candidat = models.ForeignKey('users.Candidat', on_delete=models.CASCADE)
    concours = models.ForeignKey('Concours', on_delete=models.CASCADE)
    serie = models.ForeignKey('Serie', on_delete=models.SET_NULL, null=True, blank=True, related_name='dossiers')
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
