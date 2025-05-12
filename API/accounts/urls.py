from django.urls import path
from .views import *

app_name = 'accounts'
urlpatterns = [
    path('api/login/', LoginAPIView.as_view(), name='login'),
    path('api/register/', RegisterAPIView.as_view(), name='register'),
    path('api/check_authenticate/', AuthenticateCheckAPIView.as_view(), name='check_authenticate'),
    path('api/create-account/', CreateAccountAPIView.as_view(), name='create-account'),
    path('api/check_otp_access/', CheckOtpTokenAPIView.as_view(), name='check_otp_access')
]