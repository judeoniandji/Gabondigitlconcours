from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from concours.models import Concours, Serie, Matiere, Note
from users.models import Candidat, User

class SerieViewSetPerformanceTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.concours = Concours.objects.create(
            nom="Concours Test",
            date_ouverture="2024-01-01",
            date_fermeture="2024-12-31",
            frais_inscription=10000
        )
        self.serie = Serie.objects.create(nom="Serie Test", concours=self.concours)
        self.matiere1 = Matiere.objects.create(nom="Maths", coefficient=2, serie=self.serie)
        self.matiere2 = Matiere.objects.create(nom="Physique", coefficient=3, serie=self.serie)

        self.candidat1 = Candidat.objects.create(numero_candidat="CAND001", user=User.objects.create_user("cand1", "cand1@example.com", "password"))
        self.candidat2 = Candidat.objects.create(numero_candidat="CAND002", user=User.objects.create_user("cand2", "cand2@example.com", "password"))

        Note.objects.create(candidat=self.candidat1, matiere=self.matiere1, valeur=15, etat='valide') # 15*2=30
        Note.objects.create(candidat=self.candidat1, matiere=self.matiere2, valeur=10, etat='valide') # 10*3=30
        Note.objects.create(candidat=self.candidat2, matiere=self.matiere1, valeur=12, etat='valide') # 12*2=24
        Note.objects.create(candidat=self.candidat2, matiere=self.matiere2, valeur=18, etat='valide') # 18*3=54

    def test_classement_performance(self):
        # Total Coeff = 5
        # Candidat 1: (15*2 + 10*3) / 5 = 60 / 5 = 12
        # Candidat 2: (12*2 + 18*3) / 5 = 78 / 5 = 15.6

        url = reverse('serie-classement', kwargs={'pk': self.serie.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        expected_classement = [
            {'numero_candidat': 'CAND002', 'moyenne': 15.6},
            {'numero_candidat': 'CAND001', 'moyenne': 12.0},
        ]

        # Convert response data moyennes to float for comparison
        response_data = response.json()

        # Create a mapping from numero_candidat to moyenne for easy comparison
        response_map = {item['numero_candidat']: float(item['moyenne']) for item in response_data['classement']}
        expected_map = {item['numero_candidat']: item['moyenne'] for item in expected_classement}

        self.assertEqual(len(response_map), len(expected_map))
        for numero_candidat, moyenne in expected_map.items():
            self.assertIn(numero_candidat, response_map)
            self.assertAlmostEqual(response_map[numero_candidat], moyenne, places=2)
