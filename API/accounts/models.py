from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from accounts.manager import *
from datetime import timedelta

class User(AbstractBaseUser):
    USERNAME_FIELD = 'phone'
    objects = UserManager()
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    @property
    def is_staff(self):
        return self.is_admin
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    is_email_verify = models.BooleanField(default=False)
    phone = models.CharField(
        unique=True,
        max_length=11,
        verbose_name=_('Phone Number'),
        null=False,
        blank=False
    )
    username = models.CharField(_('username'), unique=True, max_length=255, null=True, blank=True)
    email = models.EmailField(_('email'), unique=True, max_length=255, null=True, blank=True)
    first_name = models.CharField(_('first_name'), max_length=255, null=True, blank=True)
    last_name = models.CharField(_('last_name'), max_length=255, null=True, blank=True)
    image = models.ImageField(_('image'), upload_to='users__images', null=True, blank=True)
    REQUIRED_FIELDS = []

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def __str__(self):
        return self.phone

class Otp(models.Model):
    phone = models.CharField(max_length=11)
    token = models.CharField(max_length=255)
    code = models.SmallIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    @staticmethod
    def otp_clean():
        Otp.objects.filter(created_at__lt=(timezone.now() - timedelta(minutes=5))).delete()

class EmailVerifyCode(models.Model):
    user = models.ForeignKey(User, related_name='emailverifycode', on_delete=models.CASCADE)
    code = models.SmallIntegerField()
    counter = models.SmallIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    @staticmethod
    def clean_code():
        EmailVerifyCode.objects.filter(created_at__lt=(timezone.now() - timedelta(minutes=5))).delete()