from rest_framework import status
from django.urls import reverse
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from .models import Otp, EmailVerifyCode
from time import time
from .decorators_test import *
from functools import cache
from unittest.mock import patch


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


class ChangePasswordAPIViewTest(APITestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            phone='09000000000',
            username='Gorge Marting',
            email='martin@gmail.com',
            password='GMarting12345!@#$%',
        )
        self.request_data = dict({
            'current_password': 'GMarting12345!@#$%',
            'password1': 'Django12345!@#$%',
            'password2': 'Django12345!@#$%',
        })
        self.url = reverse('accounts:change-password')

    @cache
    @jwt_token
    def test_change_password_success(self):
        response = self.client.post(self.url, self.request_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['response'], 'password successfully updated')

    @cache
    @jwt_token
    def test_change_password_wrong_current_password(self):
        data = self.request_data.copy()
        data['current_password'] = 'wrong-password'
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)
        self.assertEqual(response.data['response'], 'your current password is wrong')

    @cache
    @jwt_token
    def test_change_password_same_current_password(self):
        data = self.request_data
        data['password1'] = data['password2'] = data['current_password']
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)
        self.assertEqual(response.data['response'], 'new password can not be your current password')


class GenerateEmailVerifyCodeAPIViewTest(APITestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            phone='09000000000',
            username='Gorge Marting',
            email='martin@gmail.com',
            password='GMarting12345!@#$%',
            is_email_verify=False,
        )
        self.url = reverse('accounts:generate-email-code')

    @patch('accounts.views.EmailVerifyCode.clean_code')
    @jwt_token
    def test_generate_email_verify_code_success(self, mock_clean_code):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['response'], 'send code successfully')
        self.assertEqual(str(response.data['code']).isdigit(), True)
        self.assertEqual(response.data['username'], self.user.username)
        self.assertEqual(response.data['email'], self.user.email)
        mock_clean_code.assert_called_once()

    @jwt_token
    def test_generate_email_verify_code_already_verified(self):
        self.user.is_email_verify = True
        self.user.save()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)
        self.assertEqual(response.data['response'], 'this email is already verified')


class EmailVerificationAPIViewTest(APITestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            phone='09000000000',
            username='Gorge Marting',
            email='martin@gmail.com',
            password='GMarting12345!@#$%',
            is_email_verify=False,
        )
        self.data = EmailVerifyCode.objects.create(
            user=self.user,
            code=111111,
            counter=0,
        )
        self.url = reverse('accounts:emailverification')

    @jwt_token
    def test_email_verification_success(self):
        data = {
            'code' : 111111,
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.data['response'], 'successfully verified')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @jwt_token
    def test_email_verification_wrong_code(self):
        data = {
            'code': 000000,
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)
        self.assertEqual(response.data['response'], 'invalid_code')

    @jwt_token
    def test_email_verification_already_verified(self):
        self.user.is_email_verify = True
        self.user.save()
        data = {'code': 111111}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['response'], 'not found')





