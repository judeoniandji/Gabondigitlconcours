from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from typing import cast
from .models import Concours, Serie, Matiere, Dossier, Note
from users.models import Candidat

User = get_user_model()

class JuryFlowTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        
        # Setup Concours
        self.concours = Concours._default_manager.create(
            nom="Concours Test",
            date_ouverture="2025-01-01",
            date_fermeture="2025-12-31",
            frais_inscription=10000
        )
        self.serie = Serie._default_manager.create(nom="Série A", concours=self.concours)
        self.matiere = Matiere._default_manager.create(nom="Maths", coefficient=4, serie=self.serie)
        
        # Setup Users
        self.admin = User._default_manager.create_superuser('admin', 'admin@test.com', 'pass')
        self.correcteur = User._default_manager.create_user('correcteur', 'corr@test.com', 'pass', role='correcteur')
        self.president = User._default_manager.create_user('president', 'pres@test.com', 'pass', role='president_jury')
        
        self.candidat_user = User._default_manager.create_user('candidat', 'cand@test.com', 'pass', role='candidat')
        self.candidat_profile = Candidat._default_manager.create(user=self.candidat_user, nom_complet="John Doe")
        
        # Setup Dossier
        self.dossier = Dossier._default_manager.create(
            candidat=self.candidat_profile,
            concours=self.concours,
            serie=self.serie,
            reference="REF123"
        )

    def test_anonymity_generation(self):
        # Validate dossier as admin
        self.client.force_authenticate(user=self.admin)
        res = cast(Response, self.client.patch(f'/api/concours/dossiers/{self.dossier.id}/', {'statut': 'valide'}))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        
        # Check if number generated
        self.candidat_profile.refresh_from_db()
        self.assertTrue(self.candidat_profile.numero_candidat)
        self.assertTrue(self.candidat_profile.numero_candidat.startswith('C'))
        
    def test_jury_grading_flow(self):
        # 1. Validate dossier first
        self.dossier.statut = 'valide'
        self.dossier.save()
        # Manually set number for test
        self.candidat_profile.numero_candidat = "C25-123456"
        self.candidat_profile.save()
        
        # 2. Correcteur lists candidates
        self.client.force_authenticate(user=self.correcteur)
        res = cast(Response, self.client.get(f'/api/concours/matieres/{self.matiere.id}/candidats/'))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['candidat_numero'], "C25-123456")
        # Ensure User ID is not exposed (check structure)
        self.assertNotIn('candidat_id', res.data[0]) # Wait, I didn't include it in serializer, but View manually constructs dict.
        # In View: 'candidat_numero': getattr(d.candidat, 'numero_candidat', 'Unknown'), 'note': ...
        # I did not put 'candidat_id' in the dict in the View. Good.
        
        # 3. Correcteur submits note
        res = cast(Response, self.client.post('/api/concours/notes/', {
            'matiere': self.matiere.id,
            'valeur': 15.5,
            'candidat_numero_input': "C25-123456"
        }))
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        note_id = res.data['id']
        
        # 4. Verify note status is 'brouillon'
        note = Note._default_manager.get(id=note_id)
        self.assertEqual(note.etat, 'brouillon')
        self.assertEqual(note.valeur, 15.5)
        
        # 5. President validates
        self.client.force_authenticate(user=self.president)
        res = cast(Response, self.client.put(f'/api/concours/notes/{note_id}/valider/'))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        
        note.refresh_from_db()
        self.assertEqual(note.etat, 'valide')
        self.assertEqual(note.valide_par, self.president)

    def test_classement_generation(self):
        # Manually set number for test consistency
        self.candidat_profile.numero_candidat = "C25-123456"
        self.candidat_profile.save()

        # Setup additional data
        m2 = Matiere._default_manager.create(nom="Français", coefficient=2, serie=self.serie)

        u2 = User._default_manager.create_user('c2', 'c2@test.com', 'pass', role='candidat')
        p2 = Candidat._default_manager.create(user=u2, numero_candidat="C25-000002")

        u3 = User._default_manager.create_user('c3', 'c3@test.com', 'pass', role='candidat')
        p3 = Candidat._default_manager.create(user=u3, numero_candidat="C25-000003")

        # Notes
        Note._default_manager.create(candidat=self.candidat_profile, matiere=self.matiere, valeur=12, etat='valide')
        Note._default_manager.create(candidat=self.candidat_profile, matiere=m2, valeur=10, etat='valide')

        Note._default_manager.create(candidat=p2, matiere=self.matiere, valeur=15, etat='valide')
        Note._default_manager.create(candidat=p2, matiere=m2, valeur=8, etat='valide')

        Note._default_manager.create(candidat=p3, matiere=self.matiere, valeur=10, etat='valide')
        Note._default_manager.create(candidat=p3, matiere=m2, valeur=16, etat='valide')

        # Expected averages:
        # C1 (me): (12*4 + 10*2) / 6 = 68/6 = 11.33
        # C2: (15*4 + 8*2) / 6 = 76/6 = 12.67
        # C3: (10*4 + 16*2) / 6 = 72/6 = 12.00

        self.client.force_authenticate(user=self.admin)
        res = cast(Response, self.client.get(f'/api/concours/series/{self.serie.id}/classement/'))
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        classement = res.data['classement']
        self.assertEqual(len(classement), 3)

        # Check order and values
        self.assertEqual(classement[0]['numero_candidat'], "C25-000002")
        self.assertEqual(classement[0]['moyenne'], 12.67)

        self.assertEqual(classement[1]['numero_candidat'], "C25-000003")
        self.assertEqual(classement[1]['moyenne'], 12.00)

        self.assertEqual(classement[2]['numero_candidat'], self.candidat_profile.numero_candidat)
        self.assertEqual(classement[2]['moyenne'], 11.33)
