from django.contrib.auth.backends import BaseBackend
from django.db.models import Q
from .models import User

class BaseAuthBackEnd(BaseBackend):

    def authenticate(self, request, username=None, password=None, *args, **kwargs):
        try:
            user = User.objects.filter(
                Q(username__exact = username) |
                Q(email__exact = username)
            ).first()
            if user and user.check_password(password):
                return user
            return None
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None