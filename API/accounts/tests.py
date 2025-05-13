from rest_framework import status
from django.urls import reverse
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model


class LoginAPIViewTest(APITestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='stylish',
            email='test@gmail.com',
            phone='09123456780',
            password='Test12345!@#$%'
        )
        self.url = reverse('accounts:login')

    def test_login_success(self):
        data = {
            'username': '09123456780',
            'password': 'Test12345!@#$%'
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('jwt_token', response.data)

    def test_login_incorrect_password(self):
        data = {
            'username': 'stylish',
            'password': 'WrongPassword123'
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['response'], 'incorrect password')

    def test_login_invalid_username(self):
        data = {
            'username': 'random user',
            'password': 'Test12345!@#$%'
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['response'], 'please enter a valid username, phone or email')


class RegisterAPIView(APITestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            phone='09123456789',
        )
        self.url = reverse('accounts:login')

