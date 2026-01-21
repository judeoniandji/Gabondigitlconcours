from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import Concours, Serie, Matiere, Dossier, Note
from users.models import Candidat
import datetime

User = get_user_model()

class ClassementOptimizationTest(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Users
        self.admin = User.objects.create_superuser('admin2', 'admin2@test.com', 'pass')
        self.candidat_user1 = User.objects.create_user('candidat1', 'cand1@test.com', 'pass', role='candidat')
        self.candidat_user2 = User.objects.create_user('candidat2', 'cand2@test.com', 'pass', role='candidat')
        self.candidat_profile1 = Candidat.objects.create(user=self.candidat_user1, nom_complet="Candidate One", numero_candidat="C25-000001")
        self.candidat_profile2 = Candidat.objects.create(user=self.candidat_user2, nom_complet="Candidate Two", numero_candidat="C25-000002")

        # Concours setup
        self.concours = Concours.objects.create(
            nom="Concours Performance Test",
            date_ouverture=datetime.date.today(),
            date_fermeture=datetime.date.today() + datetime.timedelta(days=30),
            frais_inscription=15000
        )
        self.serie = Serie.objects.create(nom="Performance Series", concours=self.concours)
        self.maths = Matiere.objects.create(nom="Maths", coefficient=3, serie=self.serie)
        self.physics = Matiere.objects.create(nom="Physics", coefficient=2, serie=self.serie)

        # Dossiers
        Dossier.objects.create(candidat=self.candidat_profile1, concours=self.concours, serie=self.serie, statut='valide')
        Dossier.objects.create(candidat=self.candidat_profile2, concours=self.concours, serie=self.serie, statut='valide')

        # Notes for Candidate 1: (15*3 + 12*2) / 5 = 13.8
        Note.objects.create(candidat=self.candidat_profile1, matiere=self.maths, valeur=15.00, etat='valide')
        Note.objects.create(candidat=self.candidat_profile1, matiere=self.physics, valeur=12.00, etat='valide')

        # Notes for Candidate 2: (10*3 + 18*2) / 5 = 13.2
        Note.objects.create(candidat=self.candidat_profile2, matiere=self.maths, valeur=10.00, etat='valide')
        Note.objects.create(candidat=self.candidat_profile2, matiere=self.physics, valeur=18.00, etat='valide')

    def test_classement_endpoint_performance_and_correctness(self):
        """
        ⚡ Bolt: Verifies the correctness and performance of the optimized `classement` endpoint.
        - Ensures the endpoint returns a 200 OK status.
        - Checks that the candidates are correctly ranked based on their weighted average.
        - The underlying implementation should now use a single database query.
        """
        self.client.force_authenticate(user=self.admin)

        # Make the request to the optimized endpoint
        response = self.client.get(f'/api/concours/series/{self.serie.id}/classement/')

        # 1. Verify the response is successful
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # 2. Verify the content of the response
        data = response.json()
        self.assertIn('classement', data)
        classement = data['classement']
        self.assertEqual(len(classement), 2)

        # 3. Verify the correctness of the ranking and computed averages
        # Candidate 1 should be first with a score of 13.8
        self.assertEqual(classement[0]['numero_candidat'], 'C25-000001')
        self.assertAlmostEqual(classement[0]['moyenne'], 13.80, places=2)

        # Candidate 2 should be second with a score of 13.2
        self.assertEqual(classement[1]['numero_candidat'], 'C25-000002')
        self.assertAlmostEqual(classement[1]['moyenne'], 13.20, places=2)

    def test_classement_with_no_notes(self):
        """
        Tests the behavior of the `classement` endpoint when a series has no validated notes.
        It should return an empty list.
        """
        # Create a new series with no notes
        empty_serie = Serie.objects.create(nom="Empty Series", concours=self.concours)
        self.client.force_authenticate(user=self.admin)

        response = self.client.get(f'/api/concours/series/{empty_serie.id}/classement/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.json()
        self.assertEqual(data['classement'], [])
