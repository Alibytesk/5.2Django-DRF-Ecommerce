# accounts/tests.py
from django.test import TestCase, Client
from django.urls import reverse
from unittest.mock import patch, Mock
from accounts.forms import OtpcheckForm

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


class RegisterViewTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.register_url = reverse('accounts:register')
        self.create_accounts_url = reverse('accounts:create-account')
        self.data = dict({
            'phone': '09123456780',
        })

    @patch('accounts.views.requests.post')
    def test_register_success(self, mock_post):
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {'token': 'testtoken'}
        response = self.client.post(self.register_url, data=self.data)
        self.assertEqual(response.status_code, 302)
        self.assertIn(self.create_accounts_url, response.url)
        self.assertIn('token=testtoken', response.url)
        expected_url = f'{self.create_accounts_url}?token=testtoken'
        self.assertEqual(response.url, expected_url)
        session = self.client.session
        self.assertEqual(session.get('phone'), self.data['phone'])

    @patch('accounts.views.requests.post')
    def test_register_exists_phone(self, mock_post):
        mock_post.return_value.status_code = 400
        mock_post.return_value.json.return_value = {
            'response': 'this Phone is already exists'
        }
        response = self.client.post(self.register_url, data=self.data)
        self.assertContains(response, 'this Phone is already exists')
        self.assertEqual(response.status_code, 200)
    
    @patch('accounts.views.requests.post')
    def test_register_form_validate_phone_without_begin_with_09(self, mock_post):
        response = self.client.post(self.register_url, data={'phone':'811111111111'})
        self.assertContains(response, 'phone should start with 09 number')
        self.assertEqual(response.status_code, 200)
    
    @patch('accounts.views.requests.post')
    def test_register_form_validate_phone_not_11_character(self, mock_post):
        response = self.client.post(self.register_url, data={'phone': '0911111111'})
        self.assertContains(response, 'phone must be 11 numbers')
        self.assertEqual(response.status_code, 200)

    @patch('accounts.views.requests.post')
    def test_register_form_validate_phone_send_not_numbers(self, mock):
        response = self.client.post(self.register_url, data={'phone': 'aaabbbccc'})
        self.assertContains(response, 'phone can not be character')
        self.assertEqual(response.status_code, 200)


class CreateAccountViewTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.url = reverse('accounts:create-account')
        self.redirect_url = reverse('accounts:login')
        self.data = {
            'code': '1234',
            'username': 'jk rolling',
            'email': 'rolling@gmail.com',
            'password1': 'JkRolling12345!@#$%',
            'password2': 'JkRolling12345!@#$%',
            'token': 'sometoken',
        }
        session = self.client.session
        session['phone'] = '09123456780'
        session.save()
 
    @patch('accounts.views.requests.post')
    def test_create_account_success(self, mock_post):
        mock_post.return_value.status_code = 200
        mock_post.side_effect = [
            Mock(status_code=200, json=lambda : {'is_true': True}),
            Mock(status_code=200, json=lambda : {'response': 'created account'})
        ]
        response = self.client.post(self.url, data=self.data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, self.redirect_url)

    @patch('accounts.views.requests.post')
    def test_create_account_password_does_not_match(self, mock_post):
        mock_post.side_effect = [
            Mock(status_code=200, json=lambda : {'is_true': True}),
            Mock(status_code=406, json=lambda : {'response': 'password does not match'})
        ]
        new_data = self.data.copy()
        new_data['password2'] = 'wrongpassword12345%$#@!'
        response = self.client.post(self.url, data=new_data)
        self.assertEqual(response.status_code, 200)
    
    @patch('accounts.views.requests.post')
    def test_create_account_username_email_exists(self, mock_post):
        test_cases = [
            (
                {'email': 'rolling@gmail.com', 'username': 'jk rolling'},
                'this email and username are already exists',
            ),
            (
                {'email': 'rolling@gmail.com', 'username': 'newusername'},
                'this email is already exists',
            ),
            (
                {'email': 'rolling@gmail.com', 'username': 'jk rolling'},
                'this username is already exists',
            ),
        ]
        for _, expected in test_cases:
            full_data = {**self.data, **_, 'token': 'sometoken'}
            mock_post.side_effect = [
                    Mock(status_code=200, json=lambda: {'is_true': True}),
                    Mock(status_code=406, json=lambda: {'response': expected}),
                ]
            
            with self.subTest(data=_):
                response = self.client.post(self.url, data=full_data)
                self.assertEqual(response.status_code, 200)
                self.assertContains(response, expected)

    @patch('accounts.views.requests.post')
    def test_create_account_invalid_code(self, mock_post):
        mock_post.side_effect = [
            Mock(status_code=200, json=lambda : {'is_true': True}),
            Mock(status_code=406, json=lambda : {'response': 'invalid code'}),
        ]
        new_data = self.data.copy()
        new_data['code'] = '12345'
        response = self.client.post(self.url, new_data)
        self.assertEqual(response.status_code, 200)



    def test_password_validation(self):
        test_cases = [
            (
                {'password1': 'JkRolling12345'},
                'password must contain at least one special character',
            ),
            (
                {'password1': 'JkRolling!@#$%'},
                'password must contain at least one number',
            ),
            (
                {'password1': 'jkrolling12345%$#@!'},
                'password must contain at least one uppercase character',
            ),
            (
                {'password1': 'JKROLLING12345!@#$%'},
                'password must contain at least one lowercase character',
            ),
            (
                {'password1': 'Jk1!'},
                'password must be at least 8 character',
            ),
        ]

        for override_data, expected_error in test_cases:
            form_data = {
                **self.data,
                **override_data,
                'password2': override_data['password1'],
            }
            form = OtpcheckForm(data=form_data)
            with self.subTest(password=override_data['password1']):
                self.assertFalse(form.is_valid())
                self.assertIn(expected_error, str(form.errors))

