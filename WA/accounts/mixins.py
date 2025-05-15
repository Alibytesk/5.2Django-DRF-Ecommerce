from django.shortcuts import redirect
from django.core.cache import cache
import requests
import hashlib

class AnonymousMixin:

    def dispatch(self, request, *args, **kwargs):
        if request.COOKIES.get('Authorization'):
            response = requests.post(
                url='http://127.0.0.1:8001/accounts/api/check_authenticate/',
                headers={
                    'Authorization': f'{request.COOKIES.get('Authorization')}'
                }
            )
            if response.status_code == 200:
                return redirect('/')
        return super().dispatch(request, *args, **kwargs)
    


class LoginRequiredMixin:

    def dispatch(self, request, *args, **kwargs):

        token = request.COOKIES.get('Authorization')
        if not token:
            return redirect('accounts:login')
        else:
            token_key = f'user_auth_token_{hashlib.md5(token.encode()).hexdigest()}'
            if cache.get(token_key):
                return super().dispatch(request, *args, **kwargs)
            response = requests.post(
                url='http://127.0.0.1:8001/accounts/api/check_authenticate/',
                headers=token
            )
            if response.json()['response'] == 'is_Authenticated' and response.status_code == 200:
                cache.set(key=token_key, value=True, timeout=300)
                return super().dispatch(request, *args, **kwargs)
            return redirect('accounts:login')
















        










