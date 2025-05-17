from django.urls import path
from .views import *

app_name = 'accounts'
urlpatterns = [
    path('api/login/', LoginAPIView.as_view(), name='login'),
    path('api/register/', RegisterAPIView.as_view(), name='register'),
    path('api/check_authenticate/', AuthenticateCheckAPIView.as_view(), name='check_authenticate'),
    path('api/create-account/', CreateAccountAPIView.as_view(), name='create-account'),
    path('api/check_otp_access/', CheckOtpTokenAPIView.as_view(), name='check_otp_access'),
    path('api/change-password/', ChangePasswordAPIView.as_view(), name='change-password'),
    path('api/generate-email-code/', GenerateEmailVerifyCodeAPIView.as_view(), name='generate-email-code'),
    path('api/emailverification/', EmailVerificationAPIView.as_view(), name='emailverification'),
    path('api/emailqueueauth/', EmailQueueAuthAPIView.as_view(), name='emailqueueauth'),
    path('api/emailresetpassword/<str:uid>}/<str:token>', EmailResetPasswordAPIView.as_view(), name='emailresetpassword'),
]