from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from concours.models import Concours, Serie, Matiere, Note
from users.models import User, Candidat
import datetime

class ClassementAPITest(APITestCase):
    def setUp(self):
        # Create a user for authentication
        self.user = User.objects.create_user(username='testuser', password='testpassword', role='gestionnaire')
        self.client.force_authenticate(user=self.user)

        # Create a Concours
        self.concours = Concours.objects.create(
            nom="Concours Test",
            date_ouverture=datetime.date.today(),
            date_fermeture=datetime.date.today() + datetime.timedelta(days=30),
            frais_inscription=10000
        )

        # Create a Serie
        self.serie = Serie.objects.create(nom="Serie Test", concours=self.concours)

        # Create Matieres
        self.matiere1 = Matiere.objects.create(nom="Maths", coefficient=2, serie=self.serie)
        self.matiere2 = Matiere.objects.create(nom="Physique", coefficient=3, serie=self.serie)

        # Create Candidats and Users
        self.candidat_user1 = User.objects.create_user(username='candidat1', password='testpassword', role='candidat')
        self.candidat1 = Candidat.objects.create(user=self.candidat_user1, numero_candidat='C001')

        self.candidat_user2 = User.objects.create_user(username='candidat2', password='testpassword', role='candidat')
        self.candidat2 = Candidat.objects.create(user=self.candidat_user2, numero_candidat='C002')

        # Create Notes
        Note.objects.create(candidat=self.candidat1, matiere=self.matiere1, valeur=15, etat='valide', saisi_par=self.user) # 15*2=30
        Note.objects.create(candidat=self.candidat1, matiere=self.matiere2, valeur=10, etat='valide', saisi_par=self.user) # 10*3=30 -> total 60 / 5 = 12

        Note.objects.create(candidat=self.candidat2, matiere=self.matiere1, valeur=12, etat='valide', saisi_par=self.user) # 12*2=24
        Note.objects.create(candidat=self.candidat2, matiere=self.matiere2, valeur=18, etat='valide', saisi_par=self.user) # 18*3=54 -> total 78 / 5 = 15.6

    def test_classement_endpoint(self):
        """
        Ensure the classement endpoint correctly calculates and sorts candidate averages.
        """
        url = reverse('serie-classement', kwargs={'pk': self.serie.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Expected data
        expected_classement = [
            {'numero_candidat': 'C002', 'moyenne': 15.6},
            {'numero_candidat': 'C001', 'moyenne': 12.0}
        ]

        self.assertEqual(response.data['serie'], self.serie.id)
        self.assertEqual(response.data['classement'], expected_classement)
