from .imports import *

class LoginView(AnonymousMixin, View):

    def post(self, request):
        form = LoginForm(data=request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            response = requests.post(
                url='http://127.0.0.1:8001/accounts/api/login/',
                json={
                    'username': cleaned_data.get('username'),
                    'password': cleaned_data.get('password')
                },
            )
            if response.status_code == 200:
                red = redirect('/')
                red.set_cookie(
                    key='Authorization',
                    value=f'Bearer {response.json()['jwt_token']}',
                    httponly=True,
                    max_age=3600,
                )
                return red
            elif response.status_code == 400:
                response = response.json()['response']
                form.add_error('username', response)
            else:
                form.add_error('username', 'invalid username or password')    
        return render(request, 'accounts/authentication.html', context={'form':form})


    def get(self, request):
        form = LoginForm()
        return render(request, 'accounts/authentication.html', context={'form':form})
    
class RegisterView(AnonymousMixin, View):

    def post(self, request):
        form = RegisterForm(data=request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            response = requests.post(
                url='http://127.0.0.1:8001/accounts/api/register/',
                json={'phone': cleaned_data.get('phone')}
            )
            if response.status_code == 200:
                token = response.json()['token']
                request.session['phone'] = cleaned_data['phone']
                return redirect(reverse('accounts:create-account') + f'?token={token}')
            elif response.status_code == 400:
                error = response.json()['response']
                form.add_error('phone', error)
        return render(request, 'accounts/authentication.html', context={'form':form})

    def get(self, request):
        form = RegisterForm()
        return render(request, 'accounts/authentication.html', context={'form':form})

class CreateAccountView(AnonymousMixin, View):

    def get_access(self):
        if self.request.session['phone']:
            response = requests.post(
            url='http://127.0.0.1:8001/accounts/api/check_otp_access/',
            json={
                'token': self.request.GET.get('token'),
                'phone': self.request.session.get('phone'),
            }
            )
            is_true = response.json()['is_true']
            if response.status_code == 200 and is_true:
                return True
            elif response.status_code == 406 and not is_true:
                return False
        
    def post(self, request):
        if self.get_access():
            form = OtpcheckForm(data=request.POST)
            if form.is_valid():
                cleaned_data = form.cleaned_data
                response = requests.post(
                    url='http://127.0.0.1:8001/accounts/api/create-account/',
                    json={
                        'code': cleaned_data['code'],
                        'username': cleaned_data['username'],
                        'email': cleaned_data['email'],
                        'password1': cleaned_data['password1'],
                        'password2': cleaned_data['password2'],
                        'phone': request.session['phone'],
                        'token': request.GET.get('token'),
                    }
                )
                if response.status_code == 200:
                    if request.session.get('phone'):
                        del request.session['phone']
                    return redirect('accounts:login')
                elif response.status_code == 406:
                    error = response.json()['response']
                    form.add_error('code', error)
            return render(request, 'accounts/authentication.html', context={'form':form})

    def get(self, request):
        if self.get_access():
            form = OtpcheckForm()
            return render(request, 'accounts/authentication.html', context={'form':form})
        else:
            return redirect('accounts:register')


def delete_cookies_jwt_view(request):
    red = redirect('/')
    red.delete_cookie('Authorization')
    return red


class ChangePasswordView(LoginRequiredMixin, View):

    def post(self, request):
        form = ChangePasswordForm(data=request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            if cleaned_data['password1'] == cleaned_data['password2']:
                response = requests.post(
                    url='http://127.0.0.1:8001/accounts/api/change-password/',
                    headers=dict({
                        'Authorization': str(request.COOKIES.get('Authorization')),
                    }),
                    json=dict({
                        'current_password': cleaned_data['current_password'],
                        'password1': cleaned_data['password1'],
                        'password2': cleaned_data['password2'],
                    })
                )
                if response.json()['response'] == 'password successfully updated' and response.status_code == 200:
                    messages.success(request, 'password successfully updated')
                    token = request.COOKIES.get('Authorization')
                    token_key = f'user_auth_token_{hashlib.md5(token.encode()).hexdigest()}'
                    cache.delete(token_key)
                    red = redirect('accounts:login')
                    red.delete_cookie('Authorization')
                    return red
                elif response.status_code == 406:
                    form.add_error('current_password', response.json()['response'])
            else:
                form.add_error('password2', 'confirmation password do not match')
        return render(request, 'accounts/authentication.html', context={'form':form})

    def get(self, request):
        form = ChangePasswordForm()
        return render(request, 'accounts/authentication.html', context={
            'form': form
        })


class LogoutView(View):

    def logout_user(self, request):
        token = request.COOKIES.get('Authorization')
        if token:
            token_key = f'user_auth_token_{hashlib.md5(token.encode()).hexdigest()}'
            if cache.get(token_key):
                cache.delete(token_key)
            red = redirect('/')
            red.delete_cookie('Authorization')
            return red
        return redirect('accounts:login')
    
    def post(self, request):
        return self.logout_user(request)
    
    def get(self, request):
        return self.logout_user(request)
    

class GenerateEmailVerifyCodeView(LoginRequiredMixin, View):

    def get(self, request):
        response = requests.get(
            url='http://127.0.0.1:8001/accounts/api/generate-email-code/',
            headers=dict({
                'Authorization': str(request.COOKIES.get('Authorization')),
            }),
        )
        if response.status_code == 200:
            EmailMessage(
                subject='Email Verification',
                body=render_to_string(
                    template_name='accounts/email_code.html',
                    context={
                        'username': response.json()['username'],
                        'code': response.json()['code'],
                    }
                ),
                to=[response.json()['email']],  
            ).send()
            messages.success(request, 'email verification has been sent to your email address')
            return redirect('accounts:emailverification')
        elif response.status_code == 406:
            return redirect('/')
    

class EmailVerificationView(LoginRequiredMixin, View):

    def post(self, request):
        form = EmailVerificationForm(data=request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            response = requests.post(
                url='http://127.0.0.1:8001/accounts/api/emailverification/',
                json={'code': cleaned_data['code']},
                headers={
                    'Authorization': str(request.COOKIES.get('Authorization'))
                },
            )
            if response.json()['response'] == 'successfully verified' and response.status_code == 200:
                messages.success(request, 'successfully verified email address')
                return redirect('home:home')
            elif response.json()['response'] == 'invalid_code' and response.status_code == 406:
                counter = int(request.session.get('counter', 0))
                counter += 1
                request.session['counter'] = counter
                if counter >= 3:
                    request.session['3timewrongverifycode'] = 'true'
                    del request.session['counter']
                    return redirect(reverse('accounts:emailverify'))
                form.add_error('code', response.json()['response'])
            else:
                return redirect('/')
        return render(request, 'accounts/authentication.html', context={'form':form})

    def get(self, request):
        form = EmailVerificationForm()
        key = request.session.get('3timewrongverifycode')
        if key is not None:
            del request.session['3timewrongverifycode']
            context = {'form':form, 'special_error':'send another code to your email'}
        else:
            context = {'form':form}
        response = requests.get(
            url='http://127.0.0.1:8001/accounts/api/emailverification/',
            headers={'Authorization': str(request.COOKIES.get('Authorization'))}
        )
        if response.status_code == 200 and response.json()['response'] == 'exists':
            return render(request, 'accounts/authentication.html', context)
        else:
            return redirect('/')
        

