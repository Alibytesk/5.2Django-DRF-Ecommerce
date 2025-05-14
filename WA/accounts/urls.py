from django.urls import path
from .views import *


app_name = 'accounts'
urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('create-account/', CreateAccountView.as_view(), name='create-account'),
    path('delete_jwt_cookies/', delete_cookies_jwt_view, name='delete_jwt'),
    path('change-password', ChangePasswordView.as_view(), name='change-password')
]