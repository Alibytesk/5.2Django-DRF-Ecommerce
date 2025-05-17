from django.urls import path
from .views import *


app_name = 'accounts'
urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('create-account/', CreateAccountView.as_view(), name='create-account'),
    path('delete_jwt_cookies/', delete_cookies_jwt_view, name='delete_jwt'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('emailverify/', GenerateEmailVerifyCodeView.as_view(), name='emailverify'),
    path('emailverification/', EmailVerificationView.as_view(), name='emailverification'),
    path('emailqueueauth/', EmailQueueAuthView.as_view(), name='emailqueueauth'),
    path('emailresetpassword/<str:uid>/<str:token>', EmailResetPasswordView.as_view(), name='emailresetpassword'),
    path('setpassword/', SetPasswordView.as_view(), name='setpassword'),
    path('logout/', LogoutView.as_view(), name='logout'),
]