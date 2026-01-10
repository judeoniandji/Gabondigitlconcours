from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Concours, Serie, Matiere, Note
from users.models import User, Candidat
from decimal import Decimal

class SerieClassementTest(APITestCase):
    def setUp(self):
        # Create a user for the candidate
        self.user1 = User.objects.create_user(username='candidat1', password='password', role='candidat')
        self.user2 = User.objects.create_user(username='candidat2', password='password', role='candidat')

        # Create candidates
        self.candidat1 = Candidat.objects.create(user=self.user1, numero_candidat='C1')
        self.candidat2 = Candidat.objects.create(user=self.user2, numero_candidat='C2')

        # Create a concours
        self.concours = Concours.objects.create(
            nom='Concours Test',
            date_ouverture='2024-01-01',
            date_fermeture='2024-12-31',
            frais_inscription=10000.00
        )

        # Create a serie
        self.serie = Serie.objects.create(nom='Serie Test', concours=self.concours)

        # Create matieres
        self.matiere1 = Matiere.objects.create(nom='Maths', coefficient=2.0, serie=self.serie)
        self.matiere2 = Matiere.objects.create(nom='Francais', coefficient=1.0, serie=self.serie)

        # Create notes
        Note.objects.create(candidat=self.candidat1, matiere=self.matiere1, valeur=15.0, etat='valide')
        Note.objects.create(candidat=self.candidat1, matiere=self.matiere2, valeur=12.0, etat='valide')
        Note.objects.create(candidat=self.candidat2, matiere=self.matiere1, valeur=10.0, etat='valide')
        Note.objects.create(candidat=self.candidat2, matiere=self.matiere2, valeur=18.0, etat='valide')

    def test_classement(self):
        url = reverse('serie-classement', kwargs={'pk': self.serie.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        expected_moyenne_c1 = (Decimal('15.0') * Decimal('2.0') + Decimal('12.0') * Decimal('1.0')) / (Decimal('2.0') + Decimal('1.0'))
        expected_moyenne_c2 = (Decimal('10.0') * Decimal('2.0') + Decimal('18.0') * Decimal('1.0')) / (Decimal('2.0') + Decimal('1.0'))

        classement = response.data['classement']
        self.assertEqual(len(classement), 2)

        # Check the ranking and averages
        self.assertEqual(classement[0]['numero_candidat'], 'C1')
        self.assertAlmostEqual(Decimal(classement[0]['moyenne']), expected_moyenne_c1, places=2)
        self.assertEqual(classement[1]['numero_candidat'], 'C2')
        self.assertAlmostEqual(Decimal( classement[1]['moyenne']), expected_moyenne_c2, places=2)
