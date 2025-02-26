from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status

User = get_user_model()

class UserAuthTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password123", email="test@example.com", role="student")

    def test_login_user(self):
        data = {"username": "octopus", "password": "octopus347."}
        response = self.client.post('/api/users/login/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)

    def test_protected_route_without_token(self):
        response = self.client.get('/api/protected-endpoint/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_protected_route_with_token(self):
        login_response = self.client.post('/api/users/login/', {"username": "octopus", "password": "octopus347."})
        token = login_response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.get('/api/protected-endpoint/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)