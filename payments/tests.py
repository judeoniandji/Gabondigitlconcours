from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework.response import Response as DRFResponse
from unittest.mock import patch
from typing import cast
from users.models import Candidat
from concours.models import Concours
from datetime import date, timedelta

class AirtelMsisdnValidationTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        u_data = {
            'username': 'candpay',
            'email': 'candpay@example.com',
            'password': 'Pass123!',
            'role': 'candidat',
            'telephone': '+24162345678'
        }
        self.client.post('/api/users/users/', u_data, format='json')
        token_res = cast(DRFResponse, self.client.post('/api/token/', {'username': 'candpay', 'password': 'Pass123!'}, format='json'))
        access = token_res.data.get('access')  # type: ignore[attr-defined]
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access}')
        self.concours = Concours._default_manager.create(
            nom='Test',
            description='x',
            date_ouverture=date.today(),
            date_fermeture=date.today() + timedelta(days=30),
            frais_inscription=5000
        )
        self.candidat = Candidat._default_manager.get(user__username='candpay')

    def test_airtel_invalid_msisdn(self):
        payload = {
            'msisdn': 'BAD',
            'amount': 1000,
            'reference': 'REFTEST',
            'concours_id': self.concours.id,
            'candidat_id': self.candidat.id
        }
        res = cast(DRFResponse, self.client.post('/api/payments/paiements/airtel/', payload, format='json'))
        self.assertEqual(res.status_code, 400)  # type: ignore[attr-defined]

    @patch('payments.views.initiate_airtel_payment', return_value={'ok': True})
    def test_airtel_valid_msisdn(self, mocked_call):
        payload = {
            'msisdn': '+24162345678',
            'amount': 1000,
            'reference': 'REFTEST2',
            'concours_id': self.concours.id,
            'candidat_id': self.candidat.id
        }
        res = cast(DRFResponse, self.client.post('/api/payments/paiements/airtel/', payload, format='json'))
        self.assertEqual(res.status_code, 200)  # type: ignore[attr-defined]
        self.assertIn('paiement_id', res.data)  # type: ignore[attr-defined]
