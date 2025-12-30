from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import Concours, Serie, Matiere, Note
from users.models import User, Candidat
import decimal

class SerieViewSetClassementTest(APITestCase):
    def setUp(self):
        # Create a user for authentication if needed
        self.user = User.objects.create_user(username='testuser', password='testpassword', role='gestionnaire')
        self.client.force_authenticate(user=self.user)

        # Create Concours
        self.concours = Concours.objects.create(
            nom="Concours Test",
            date_ouverture="2024-01-01",
            date_fermeture="2024-12-31",
            frais_inscription=10000
        )

        # Create Serie
        self.serie = Serie.objects.create(nom="Serie Test", concours=self.concours)

        # Create Matieres
        self.math = Matiere.objects.create(nom="Math", coefficient=decimal.Decimal('2.0'), serie=self.serie)
        self.physics = Matiere.objects.create(nom="Physics", coefficient=decimal.Decimal('1.5'), serie=self.serie)

        # Create Candidats
        self.user1 = User.objects.create_user(username='candidat1', password='testpassword', role='candidat')
        self.candidat1 = Candidat.objects.create(user=self.user1, numero_candidat='C1')

        self.user2 = User.objects.create_user(username='candidat2', password='testpassword', role='candidat')
        self.candidat2 = Candidat.objects.create(user=self.user2, numero_candidat='C2')

        # Create Notes
        Note.objects.create(candidat=self.candidat1, matiere=self.math, valeur=decimal.Decimal('15.0'), etat='valide')
        Note.objects.create(candidat=self.candidat1, matiere=self.physics, valeur=decimal.Decimal('12.0'), etat='valide')
        Note.objects.create(candidat=self.candidat2, matiere=self.math, valeur=decimal.Decimal('10.0'), etat='valide')
        Note.objects.create(candidat=self.candidat2, matiere=self.physics, valeur=decimal.Decimal('18.0'), etat='valide')


    def test_classement_endpoint(self):
        url = reverse('serie-classement', kwargs={'pk': self.serie.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Expected data
        # Candidat 1: (15 * 2) + (12 * 1.5) = 30 + 18 = 48. Moyenne = 48 / 3.5 = 13.71
        # Candidat 2: (10 * 2) + (18 * 1.5) = 20 + 27 = 47. Moyenne = 47 / 3.5 = 13.43
        expected_classement = [
            {'numero_candidat': 'C1', 'moyenne': 13.71},
            {'numero_candidat': 'C2', 'moyenne': 13.43},
        ]

        response_data = response.json()
        self.assertEqual(response_data['serie'], self.serie.id)

        # Convert response averages to float for comparison
        for item in response_data['classement']:
            item['moyenne'] = float(item['moyenne'])

        self.assertEqual(len(response_data['classement']), 2)

        # Check sorting
        self.assertGreater(response_data['classement'][0]['moyenne'], response_data['classement'][1]['moyenne'])

        # Check values
        self.assertEqual(response_data['classement'][0]['numero_candidat'], 'C1')
        self.assertAlmostEqual(response_data['classement'][0]['moyenne'], 13.71, places=2)
        self.assertEqual(response_data['classement'][1]['numero_candidat'], 'C2')
        self.assertAlmostEqual(response_data['classement'][1]['moyenne'], 13.43, places=2)
