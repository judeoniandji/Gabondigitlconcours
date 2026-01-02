from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from concours.models import Concours, Serie, Matiere, Note
from users.models import User, Candidat
from decimal import Decimal

class SerieViewSetClassementTest(APITestCase):
    def setUp(self):
        # Create users and candidates
        self.user1 = User.objects.create_user(username='candidat1', password='password', role='candidat')
        self.candidat1 = Candidat.objects.create(user=self.user1, numero_candidat='C1')

        self.user2 = User.objects.create_user(username='candidat2', password='password', role='candidat')
        self.candidat2 = Candidat.objects.create(user=self.user2, numero_candidat='C2')

        # Create concours
        self.concours = Concours.objects.create(
            nom='Concours Test',
            date_ouverture='2024-01-01',
            date_fermeture='2024-12-31',
            frais_inscription=100.00
        )

        # Create serie
        self.serie = Serie.objects.create(nom='Serie A', concours=self.concours)

        # Create matieres
        self.math = Matiere.objects.create(nom='Math', coefficient=2.0, serie=self.serie)
        self.physics = Matiere.objects.create(nom='Physics', coefficient=1.5, serie=self.serie)

        # Create notes for candidat1
        Note.objects.create(candidat=self.candidat1, matiere=self.math, valeur=Decimal('15.0'), etat='valide')
        Note.objects.create(candidat=self.candidat1, matiere=self.physics, valeur=Decimal('12.0'), etat='valide')

        # Create notes for candidat2
        Note.objects.create(candidat=self.candidat2, matiere=self.math, valeur=Decimal('18.0'), etat='valide')
        Note.objects.create(candidat=self.candidat2, matiere=self.physics, valeur=Decimal('10.0'), etat='valide')

    def test_classement_endpoint(self):
        """
        Tests the classement endpoint to ensure it returns the correct ranking and averages.
        """
        url = reverse('serie-classement', kwargs={'pk': self.serie.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Expected averages
        # Candidat 1: (15 * 2 + 12 * 1.5) / (2 + 1.5) = (30 + 18) / 3.5 = 48 / 3.5 = 13.71
        # Candidat 2: (18 * 2 + 10 * 1.5) / (2 + 1.5) = (36 + 15) / 3.5 = 51 / 3.5 = 14.57
        expected_classement = [
            {'numero_candidat': 'C2', 'moyenne': 14.57},
            {'numero_candidat': 'C1', 'moyenne': 13.71},
        ]

        # Round the response data for comparison
        response_data = response.json()
        classement = response_data.get('classement', [])
        for item in classement:
            item['moyenne'] = round(item['moyenne'], 2)

        self.assertEqual(len(classement), 2)
        self.assertEqual(classement, expected_classement)
