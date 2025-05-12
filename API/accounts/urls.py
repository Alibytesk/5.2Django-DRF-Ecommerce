from django.urls import path
from .views import *

app_name = 'accounts'
urlpatterns = [
    path('api/login/', LoginAPIView.as_view(), name='login'),
    path('api/check_authenticate/', AuthenticateCheckAPIView.as_view(), name='check_authenticate')
]