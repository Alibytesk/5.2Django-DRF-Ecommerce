from django.shortcuts import redirect
import requests

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