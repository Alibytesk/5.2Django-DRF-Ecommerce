from rest_framework import status
from django.urls import reverse
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from .models import Otp
from time import time


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



class RegisterAPIViewTest(APITestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='stylish',
            email='test@gmail.com',
            phone='09123456780',
            password='Test12345!@#$%'
        )
        self.url = reverse('accounts:register')

    def test_register_success(self):
        data = {
            'phone': '09876543210',
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, 'token')

    def test_register_phone_exists(self):
        data = {
            'phone': '09123456780',
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(response.data['response'], 'this Phone is already exists')


class CheckOtpTokenAPIViewTest(APITestCase):

    def setUp(self):
        self._objects = Otp.objects.create(
            code='1234',
            phone='09123456780',
            token='i love testing more than myself'
        )
        self.url = reverse('accounts:check_otp_access')

    def test_check_otp_token_success(self):
        data = {
            'token' : 'i love testing more than myself',
            'phone': '09123456780',
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, 'is_true')

    def test_check_invalid_code_token(self):
        data = {
            'token' : ' love testing more than myself',
            'phone': '09123456780',
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)
        is_False = response.data['is_true']
        self.assertEqual(False, is_False)


class CreateAccountAPIViewTest(APITestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            phone='09000000000',
            username= 'Gorge Marting',
            email= 'martin@gmail.com',
            password= 'GMarting12345!@#$%',
        )
        self.otp_objects = Otp.objects.create(
            code='1234',
            phone='09123456780',
            token='i love testing more than myself'
        )
        self.url = reverse('accounts:create-account')


    def test_create_account_success(self):
        data = {
            'phone': '09123456780',
            'username': 'jk rolling',
            'email': 'rolling@gmail.com',
            'password1': 'JkRolling12345!@#$%',
            'password2': 'JkRolling12345!@#$%',
            "code" : '1234',
            "token": 'i love testing more than myself',
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(response.data['response'], 'created account')

    def test_create_account_invalid_code(self):
        data = {
            "code": '12',
            "token": 'i love testing more than myself',
            'phone': '09123456780',
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)
        self.assertIn(response.data['response'], 'invalid code')

    def test_create_account_email_exists(self):
        data = {
            'phone': '09123456780',
            'password1': 'JkRolling12345!@#$%',
            'password2': 'JkRolling12345!@#$%',
            'username': 'jk rolling',
            'email': 'martin@gmail.com',
            "code" : '1234',
            "token": 'i love testing more than myself',
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)
        self.assertIn('this email is already exists', response.data['response'])
