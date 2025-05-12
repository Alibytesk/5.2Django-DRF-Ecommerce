# accounts/tests.py
from django.test import TestCase, Client
from django.urls import reverse
from unittest.mock import patch

class LoginViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.login_url = reverse('accounts:login')  
        self.data = {
            'username': 'testuser',
            'password': 'Test@1234'
        }

    @patch('accounts.views.requests.post') 
    def test_login_success(self, mock_post):
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {
            'jwt_token': 'mocked.jwt.token'
        }

        response = self.client.post(self.login_url, data=self.data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/')
        self.assertIn('Authorization', response.cookies)

    @patch('accounts.views.requests.post')
    def test_login_wrong_password(self, mock_post):
        mock_post.return_value.status_code = 400
        mock_post.return_value.json.return_value = {
            'response': 'incorrect password'
        }
        response = self.client.post(self.login_url, data=self.data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'incorrect password')

    @patch('accounts.views.requests.post')
    def test_login_invalid_username(self, mock_post):
        mock_post.return_value.status_code = 400
        mock_post.return_value.json.return_value = {
            'response': 'please enter a valid username, phone or email'
        }

        response = self.client.post(self.login_url, data=self.data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'please enter a valid username')
