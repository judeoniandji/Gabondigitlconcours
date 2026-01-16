from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Concours, Serie, Matiere, Note
from users.models import User, Candidat
from decimal import Decimal

class SerieClassementAPITestCase(APITestCase):
    def setUp(self):
        # Create test users
        self.user1 = User.objects.create_user(username='candidat1', password='password', role='candidat')
        self.user2 = User.objects.create_user(username='candidat2', password='password', role='candidat')

        # Create test candidats
        self.candidat1 = Candidat.objects.create(user=self.user1, numero_candidat='CAND001')
        self.candidat2 = Candidat.objects.create(user=self.user2, numero_candidat='CAND002')

        # Create a test concours
        self.concours = Concours.objects.create(
            nom='Concours Test',
            date_ouverture='2024-01-01',
            date_fermeture='2024-12-31',
            frais_inscription=10000.00
        )

        # Create a test serie
        self.serie = Serie.objects.create(nom='Serie Test', concours=self.concours)

        # Create test matieres
        self.math = Matiere.objects.create(nom='Mathématiques', coefficient=Decimal('3.0'), serie=self.serie)
        self.francais = Matiere.objects.create(nom='Français', coefficient=Decimal('2.0'), serie=self.serie)

        # Create test notes
        # Candidat 1: Math=15, Francais=12. Moyenne = (15*3 + 12*2) / (3+2) = 13.8
        Note.objects.create(candidat=self.candidat1, matiere=self.math, valeur=Decimal('15.0'), etat='valide')
        Note.objects.create(candidat=self.candidat1, matiere=self.francais, valeur=Decimal('12.0'), etat='valide')

        # Candidat 2: Math=10, Francais=18. Moyenne = (10*3 + 18*2) / (3+2) = 13.2
        Note.objects.create(candidat=self.candidat2, matiere=self.math, valeur=Decimal('10.0'), etat='valide')
        Note.objects.create(candidat=self.candidat2, matiere=self.francais, valeur=Decimal('18.0'), etat='valide')

    def test_classement_calculation(self):
        """
        Verify that the 'classement' endpoint calculates averages correctly and
        returns a properly sorted list of candidats.
        """
        url = reverse('serie-classement', kwargs={'pk': self.serie.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        expected_classement = [
            {'numero_candidat': 'CAND001', 'moyenne': 13.8},
            {'numero_candidat': 'CAND002', 'moyenne': 13.2},
        ]

        self.assertEqual(response.data['serie'], self.serie.id)
        # Round the moyennes in the response for comparison
        response_classement = [
            {'numero_candidat': item['numero_candidat'], 'moyenne': round(item['moyenne'], 2)}
            for item in response.data['classement']
        ]

        self.assertEqual(len(response_classement), 2)
        self.assertEqual(response_classement, expected_classement)
