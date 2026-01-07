from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Concours, Serie, Matiere, Note
from users.models import User, Candidat
import datetime
from decimal import Decimal

class SerieClassementAPITest(APITestCase):
    def setUp(self):
        # Create Users and Candidates
        self.user1 = User.objects.create_user(username='candidat1', password='password', role='candidat')
        self.candidat1 = Candidat.objects.create(user=self.user1, numero_candidat='CAND001')

        self.user2 = User.objects.create_user(username='candidat2', password='password', role='candidat')
        self.candidat2 = Candidat.objects.create(user=self.user2, numero_candidat='CAND002')

        # Create Concours
        self.concours = Concours.objects.create(
            nom="Concours Test",
            date_ouverture=datetime.date.today(),
            date_fermeture=datetime.date.today() + datetime.timedelta(days=30),
            frais_inscription=Decimal('10000.00')
        )

        # Create Serie
        self.serie = Serie.objects.create(nom="Serie A", concours=self.concours)

        # Create Matieres
        self.maths = Matiere.objects.create(nom="Maths", coefficient=Decimal('3.0'), serie=self.serie)
        self.francais = Matiere.objects.create(nom="Français", coefficient=Decimal('2.0'), serie=self.serie)

        # Create Notes for Candidat 1
        Note.objects.create(candidat=self.candidat1, matiere=self.maths, valeur=Decimal('15.0'), etat='valide') # 15*3=45
        Note.objects.create(candidat=self.candidat1, matiere=self.francais, valeur=Decimal('12.0'), etat='valide') # 12*2=24 -> Total=69. Moyenne=69/5=13.8

        # Create Notes for Candidat 2
        Note.objects.create(candidat=self.candidat2, matiere=self.maths, valeur=Decimal('10.0'), etat='valide') # 10*3=30
        Note.objects.create(candidat=self.candidat2, matiere=self.francais, valeur=Decimal('18.0'), etat='valide') # 18*2=36 -> Total=66. Moyenne=66/5=13.2

    def test_classement_endpoint(self):
        """
        Ensure the classement endpoint returns the correct ranking of candidates.
        """
        # Create a user with permissions to view the endpoint if needed
        self.admin_user = User.objects.create_user(username='admin', password='password', role='admin')
        self.client.force_authenticate(user=self.admin_user)

        url = reverse('serie-classement', kwargs={'pk': self.serie.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()
        self.assertIn('classement', data)
        classement = data['classement']

        # Verify the number of candidates in the ranking
        self.assertEqual(len(classement), 2)

        # Verify the order and scores
        # Candidat 1 should be first with a weighted average of 13.8
        self.assertEqual(classement[0]['numero_candidat'], 'CAND001')
        self.assertEqual(classement[0]['moyenne'], 13.8)

        # Candidat 2 should be second with a weighted average of 13.2
        self.assertEqual(classement[1]['numero_candidat'], 'CAND002')
        self.assertEqual(classement[1]['moyenne'], 13.2)
