from datetime import date
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Concours, Serie, Matiere, Note
from users.models import Candidat

User = get_user_model()

class SerieViewSetClassementTest(APITestCase):
    def setUp(self):
        # Create users and candidates
        self.user1 = User.objects.create_user(username='candidat1', password='password', role='candidat')
        self.candidat1 = Candidat.objects.create(user=self.user1, numero_candidat='C1')

        self.user2 = User.objects.create_user(username='candidat2', password='password', role='candidat')
        self.candidat2 = Candidat.objects.create(user=self.user2, numero_candidat='C2')

        # Create concours and serie
        self.concours = Concours.objects.create(
            nom='Test Concours',
            date_ouverture=date.today(),
            date_fermeture=date.today(),
            frais_inscription=10000
        )
        self.serie = Serie.objects.create(concours=self.concours, nom='Test Serie')

        # Create matieres with coefficients
        self.math = Matiere.objects.create(serie=self.serie, nom='Math', coefficient=3)
        self.francais = Matiere.objects.create(serie=self.serie, nom='Francais', coefficient=2)

        # Total coefficient sum is 5

        # Create notes for candidat1:
        # Math: 15 * 3 = 45
        # Francais: 10 * 2 = 20
        # Total points = 65, Moyenne = 65 / 5 = 13
        Note.objects.create(candidat=self.candidat1, matiere=self.math, valeur=15, etat='valide')
        Note.objects.create(candidat=self.candidat1, matiere=self.francais, valeur=10, etat='valide')

        # Create notes for candidat2:
        # Math: 12 * 3 = 36
        # Francais: 18 * 2 = 36
        # Total points = 72, Moyenne = 72 / 5 = 14.4
        Note.objects.create(candidat=self.candidat2, matiere=self.math, valeur=12, etat='valide')
        Note.objects.create(candidat=self.candidat2, matiere=self.francais, valeur=18, etat='valide')


    def test_classement_endpoint(self):
        """
        Tests the classement endpoint to ensure it returns the correct weighted averages.
        """
        url = f'/api/concours/series/{self.serie.id}/classement/'
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        classement = response.data.get('classement', [])
        self.assertEqual(len(classement), 2)

        # Expected classement: Candidat2 (14.4) > Candidat1 (13.0)

        # Check first place
        self.assertEqual(classement[0]['candidat__numero_candidat'], 'C2')
        self.assertAlmostEqual(float(classement[0]['moyenne']), 14.4)

        # Check second place
        self.assertEqual(classement[1]['candidat__numero_candidat'], 'C1')
        self.assertAlmostEqual(float(classement[1]['moyenne']), 13.0)
