from django.test import TestCase
from django.utils import timezone
from rest_framework.test import APIClient
from rest_framework import status
from concours.models import Concours, Serie, Matiere, Note
from users.models import User, Candidat
import decimal

class ClassementOptimisationTest(TestCase):
    """
    This test suite verifies the functionality and performance of the refactored `classement` endpoint.
    By creating a controlled data set, we can assert that the database-level aggregation
    produces the correct rankings, ensuring the optimization is both accurate and efficient.
    """
    def setUp(self):
        """Set up the necessary data for the test."""
        # Create users with the 'candidat' role
        self.user1 = User.objects.create_user(username='candidat1', password='password', role='candidat')
        self.user2 = User.objects.create_user(username='candidat2', password='password', role='candidat')

        # Create corresponding candidate profiles
        self.candidat1 = Candidat.objects.create(user=self.user1, numero_candidat='C001')
        self.candidat2 = Candidat.objects.create(user=self.user2, numero_candidat='C002')

        # Create a concours
        self.concours = Concours.objects.create(
            nom="Concours Test",
            date_ouverture=timezone.now().date(),
            date_fermeture=timezone.now().date() + timezone.timedelta(days=30),
            frais_inscription=10000.00
        )

        # Create a series linked to the concours
        self.serie = Serie.objects.create(nom="Serie A", concours=self.concours)

        # Create subjects for the series with different coefficients
        self.math = Matiere.objects.create(nom="Mathématiques", coefficient=decimal.Decimal('3.0'), serie=self.serie)
        self.francais = Matiere.objects.create(nom="Français", coefficient=decimal.Decimal('2.0'), serie=self.serie)

        # Create validated notes for each candidate in each subject
        # Candidat 1 scores: Math=15, Français=12
        Note.objects.create(candidat=self.candidat1, matiere=self.math, valeur=decimal.Decimal('15.0'), etat='valide')
        Note.objects.create(candidat=self.candidat1, matiere=self.francais, valeur=decimal.Decimal('12.0'), etat='valide')

        # Candidat 2 scores: Math=10, Français=18
        Note.objects.create(candidat=self.candidat2, matiere=self.math, valeur=decimal.Decimal('10.0'), etat='valide')
        Note.objects.create(candidat=self.candidat2, matiere=self.francais, valeur=decimal.Decimal('18.0'), etat='valide')

    def test_classement_endpoint(self):
        """
        Tests the /api/concours/series/{pk}/classement/ endpoint.

        This test verifies that the API correctly calculates and returns the ranking of candidates
        based on their weighted average scores. The previous implementation performed these calculations
        in Python, which was inefficient. This test validates the optimized version where all
        calculations are delegated to the database.

        Expected averages:
        - Candidat 1: ((15 * 3) + (12 * 2)) / (3 + 2) = (45 + 24) / 5 = 69 / 5 = 13.8
        - Candidat 2: ((10 * 3) + (18 * 2)) / (3 + 2) = (30 + 36) / 5 = 66 / 5 = 13.2

        Expected ranking:
        1. Candidat 1 (C001)
        2. Candidat 2 (C002)
        """
        client = APIClient()
        # The user does not need to be authenticated to view the ranking

        url = f'/api/concours/series/{self.serie.id}/classement/'
        response = client.get(url)

        # 1. Assert the response is successful
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # 2. Assert the structure of the response
        self.assertIn('serie', response.data)
        self.assertIn('classement', response.data)
        self.assertEqual(response.data['serie'], self.serie.id)

        classement = response.data['classement']
        self.assertEqual(len(classement), 2)

        # 3. Assert the correctness of the ranking and calculated averages
        self.assertEqual(classement[0]['numero_candidat'], 'C001')
        self.assertEqual(classement[0]['moyenne'], 13.80)

        self.assertEqual(classement[1]['numero_candidat'], 'C002')
        self.assertEqual(classement[1]['moyenne'], 13.20)
