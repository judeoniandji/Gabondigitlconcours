from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Concours, Serie, Matiere, Note
from users.models import User, Candidat
from decimal import Decimal
import datetime

class SerieViewSetClassementTest(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Create Users and Candidates
        self.user1 = User.objects.create_user(username='candidat1', password='password', role='candidat')
        self.candidat1 = Candidat.objects.create(user=self.user1, numero_candidat='C1')

        self.user2 = User.objects.create_user(username='candidat2', password='password', role='candidat')
        self.candidat2 = Candidat.objects.create(user=self.user2, numero_candidat='C2')

        # Create Concours
        self.concours = Concours.objects.create(
            nom='Concours Test',
            date_ouverture=datetime.date.today(),
            date_fermeture=datetime.date.today() + datetime.timedelta(days=30),
            frais_inscription=100.00
        )

        # Create Serie
        self.serie = Serie.objects.create(nom='Serie Test', concours=self.concours)

        # Create Matieres
        self.math = Matiere.objects.create(nom='Math', coefficient=Decimal('2.0'), serie=self.serie)
        self.francais = Matiere.objects.create(nom='Francais', coefficient=Decimal('1.0'), serie=self.serie)

        # Create Notes
        # Candidat 1: Math=15, Francais=12 -> (15*2 + 12*1) / 3 = 14
        Note.objects.create(candidat=self.candidat1, matiere=self.math, valeur=Decimal('15.00'), etat='valide')
        Note.objects.create(candidat=self.candidat1, matiere=self.francais, valeur=Decimal('12.00'), etat='valide')

        # Candidat 2: Math=10, Francais=18 -> (10*2 + 18*1) / 3 = 12.67
        Note.objects.create(candidat=self.candidat2, matiere=self.math, valeur=Decimal('10.00'), etat='valide')
        Note.objects.create(candidat=self.candidat2, matiere=self.francais, valeur=Decimal('18.00'), etat='valide')

    def test_classement_calculation(self):
        url = f'/api/concours/series/{self.serie.id}/classement/'
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['serie'], self.serie.id)

        classement = response.data['classement']
        self.assertEqual(len(classement), 2)

        # Check ranking and averages
        self.assertEqual(classement[0]['numero_candidat'], 'C1')
        self.assertAlmostEqual(classement[0]['moyenne'], 14.00, places=2)

        self.assertEqual(classement[1]['numero_candidat'], 'C2')
        self.assertAlmostEqual(classement[1]['moyenne'], 12.67, places=2)
