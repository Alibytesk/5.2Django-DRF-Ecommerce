from django.urls import path
from .views import *


app_name = 'accounts'
urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('delete_jwt_cookies', delete_cookies_jwt_view, name='delete_jwt'),
]