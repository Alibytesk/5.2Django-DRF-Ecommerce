#django
from django.shortcuts import render, redirect
from django.views.generic.base import View
from django.db.models import Q
from django.http import HttpResponse
#apps
from .forms import *

import requests


class LoginView(View):

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
        if request.COOKIES.get('Authorization'):
            response = requests.post(
                url='http://127.0.0.1:8001/accounts/api/check_authenticate/',
                headers={
                    'Authorization': f'{request.COOKIES.get('Authorization')}'
                }
            )
            if response.status_code == 200:
                return redirect('/')
        return render(request, 'accounts/authentication.html', context={'form':form})
    


def delete_cookies_jwt_view(request):
    red = redirect('/')
    red.delete_cookie('Authorization')
    return red