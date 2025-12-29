from django.test import TestCase
from rest_framework.test import APIClient

class UserPhoneValidationTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_candidate_requires_phone(self):
        data = {
            'username': 'cand_notel',
            'email': 'cand_notel@example.com',
            'password': 'Pass123!',
            'role': 'candidat'
        }
        res = self.client.post('/api/users/users/', data, format='json')
        self.assertEqual(res.status_code, 400)
        self.assertIn('telephone', res.data)

    def test_candidate_accepts_valid_phone_formats(self):
        for tel in ['06234567', '+24162345678']:
            data = {
                'username': f'cand_{tel[-4:]}',
                'email': f'cand_{tel[-4:]}@example.com',
                'password': 'Pass123!',
                'role': 'candidat',
                'telephone': tel
            }
            res = self.client.post('/api/users/users/', data, format='json')
            self.assertEqual(res.status_code, 201)
