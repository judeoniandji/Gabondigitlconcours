from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from concours.models import Concours, Serie, Matiere, Note
from users.models import User, Candidat
import datetime

class ClassementPerformanceTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin_user = User.objects.create_superuser('admin', 'admin@example.com', 'password')

        self.concours = Concours.objects.create(
            nom='Concours Test',
            date_ouverture=datetime.date.today() - datetime.timedelta(days=1),
            date_fermeture=datetime.date.today() + datetime.timedelta(days=1),
            frais_inscription=100.0
        )
        self.serie = Serie.objects.create(nom='Serie Test', concours=self.concours)
        self.matiere1 = Matiere.objects.create(nom='Maths', coefficient=2, serie=self.serie)
        self.matiere2 = Matiere.objects.create(nom='Français', coefficient=1, serie=self.serie)

        self.candidat1 = Candidat.objects.create(
            user=User.objects.create_user('candidat1', 'candidat1@example.com', 'password', role='candidat', is_active=True),
            numero_candidat='C001'
        )
        self.candidat2 = Candidat.objects.create(
            user=User.objects.create_user('candidat2', 'candidat2@example.com', 'password', role='candidat', is_active=True),
            numero_candidat='C002'
        )

        Note.objects.create(candidat=self.candidat1, matiere=self.matiere1, valeur=15, etat='valide', saisi_par=self.admin_user)
        Note.objects.create(candidat=self.candidat1, matiere=self.matiere2, valeur=12, etat='valide', saisi_par=self.admin_user)
        Note.objects.create(candidat=self.candidat2, matiere=self.matiere1, valeur=10, etat='valide', saisi_par=self.admin_user)
        Note.objects.create(candidat=self.candidat2, matiere=self.matiere2, valeur=18, etat='valide', saisi_par=self.admin_user)

        self.client.force_authenticate(user=self.admin_user)

    def test_classement_performance_and_correctness(self):
        # On s'attend à ce que le calcul soit correct
        # Candidat 1: (15*2 + 12*1) / (2+1) = 42 / 3 = 14.0
        # Candidat 2: (10*2 + 18*1) / (2+1) = 38 / 3 = 12.67

        url = reverse('serie-classement', kwargs={'pk': self.serie.pk})

        # Utilisation de assertNumQueries pour vérifier l'efficacité
        with self.assertNumQueries(3):
            response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        classement = response.data.get('classement', [])
        self.assertEqual(len(classement), 2)

        # Vérification du classement et des moyennes
        self.assertEqual(classement[0]['numero_candidat'], 'C001')
        self.assertAlmostEqual(classement[0]['moyenne'], 14.0, places=2)

        self.assertEqual(classement[1]['numero_candidat'], 'C002')
        self.assertAlmostEqual(classement[1]['moyenne'], 12.67, places=2)
