from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Concours, Serie, Matiere, Note
from users.models import User, Candidat
import decimal

class ClassementEndpointTest(APITestCase):
    def setUp(self):
        # Create users for candidates
        self.user1 = User.objects.create_user(username='candidat1', password='password', role='candidat')
        self.user2 = User.objects.create_user(username='candidat2', password='password', role='candidat')
        self.user3 = User.objects.create_user(username='candidat3', password='password', role='candidat')

        # Create candidates
        self.candidat1 = Candidat.objects.create(user=self.user1, numero_candidat='C1')
        self.candidat2 = Candidat.objects.create(user=self.user2, numero_candidat='C2')
        self.candidat3 = Candidat.objects.create(user=self.user3, numero_candidat='C3')

        # Create a Concours
        self.concours = Concours.objects.create(nom='Test Concours', date_ouverture='2024-01-01', date_fermeture='2024-12-31', frais_inscription=1000)

        # Create a Serie
        self.serie = Serie.objects.create(nom='Test Serie', concours=self.concours)

        # Create Matieres with coefficients
        self.math = Matiere.objects.create(nom='Math', coefficient=decimal.Decimal('3.0'), serie=self.serie)
        self.physics = Matiere.objects.create(nom='Physics', coefficient=decimal.Decimal('2.0'), serie=self.serie)

        # Create Notes for each candidate
        # Candidat 1 scores
        Note.objects.create(candidat=self.candidat1, matiere=self.math, valeur=decimal.Decimal('15.0'), etat='valide')
        Note.objects.create(candidat=self.candidat1, matiere=self.physics, valeur=decimal.Decimal('12.0'), etat='valide')

        # Candidat 2 scores
        Note.objects.create(candidat=self.candidat2, matiere=self.math, valeur=decimal.Decimal('18.0'), etat='valide')
        Note.objects.create(candidat=self.candidat2, matiere=self.physics, valeur=decimal.Decimal('16.0'), etat='valide')

        # Candidat 3 scores (lower)
        Note.objects.create(candidat=self.candidat3, matiere=self.math, valeur=decimal.Decimal('10.0'), etat='valide')
        Note.objects.create(candidat=self.candidat3, matiere=self.physics, valeur=decimal.Decimal('8.0'), etat='valide')

    def test_classement_endpoint(self):
        # URL for the classement endpoint
        url = reverse('serie-classement', kwargs={'pk': self.serie.pk})

        # Make the request
        response = self.client.get(url)

        # Assert the response status
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert the structure of the response
        self.assertIn('serie', response.data)
        self.assertIn('classement', response.data)
        self.assertEqual(response.data['serie'], self.serie.pk)

        # Expected averages
        # Candidat 1: (15 * 3 + 12 * 2) / (3 + 2) = (45 + 24) / 5 = 13.8
        # Candidat 2: (18 * 3 + 16 * 2) / (3 + 2) = (54 + 32) / 5 = 17.2
        # Candidat 3: (10 * 3 + 8 * 2) / (3 + 2) = (30 + 16) / 5 = 9.2
        expected_classement = [
            {'numero_candidat': 'C2', 'moyenne': 17.2},
            {'numero_candidat': 'C1', 'moyenne': 13.8},
            {'numero_candidat': 'C3', 'moyenne': 9.2},
        ]

        # Assert the classement is correct and in the right order
        self.assertEqual(len(response.data['classement']), 3)
        self.assertEqual(response.data['classement'], expected_classement)
