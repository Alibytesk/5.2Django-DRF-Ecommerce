from django.db import models
import itertools
import re

class UserManager(models.Manager):

    def create_user(self, phone, username=None, email=None, password=None, **extra_fields):
        phone = self.normalize_phone(phone)
        if not username and not email:
            user = self.model(phone=phone, username=None, email=None, **extra_fields)
        elif not email:
            username = self.normalize_username(username)
            user = self.model(phone=phone, username=username, email=None, **extra_fields)
        elif not username:
            email = self.normalize_email(email)
            user = self.model(phone=phone, username=None, email=email, **extra_fields)
        elif username and email:
            email, username = self.normalize_email(email), self.normalize_username(username)
            user = self.model(phone=phone, username=username, email=email, **extra_fields)
        else:
            raise ValueError('invalid email or username')
        password = self.normalize_password(password=password)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, username=None, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_admin', True)
        return self.create_user(phone, username, email, password, **extra_fields)

    def get_by_natural_key(self, username):
        return self.get(**{self.model.USERNAME_FIELD: username})

    async def aget_by_natural_key(self, username):
        return await self.aget(**{self.model.USERNAME_FIELD: username})

    @staticmethod
    def normalize_password(password: str):
        if not password:
            raise ValueError('invalid password')
        errors, _allowed = list(), '!@#$%^&*'
        if not any(i in _allowed for i in password):
            errors.append('password must contain at least one special character')
        if not any(i.isdigit() for i in password):
            errors.append('password must contain at least one number')
        if not any(i.isupper() for i in password):
            errors.append('password must contain at least one uppercase character')
        if not any(i.lower() for i in password):
            errors.append('password must contain at least one lowercase character')
        if not errors:
            return password
        raise ValueError('; '.join(errors))

    @staticmethod
    def normalize_phone(phone: str):
        if not phone:
            raise ValueError('invalid phone')
        phone = UserManager.convert_fa_digits_to_en(phone=phone)
        phone = re.sub(r'\D', '', phone)
        if phone.isdigit() and len(phone) == 11 and phone.startswith('09'):
            return phone
        raise ValueError('invalid phone number')

    @staticmethod
    def convert_fa_digits_to_en(phone: str):
        DIGITS = dict({
            '۰':'0','۱':'1','۲':'2','۳':'3','۴':'4','۵':'5','۶':'6','۷':'7','۸':'8','۹':'9'
        })
        for per, eng in DIGITS.items():
            phone = str(phone.replace(per, eng))
        return phone

    @staticmethod
    def normalize_username(username: str):
        username = username.strip().lower()
        allowed = set('abcdefghijklmnopqrstuvwxyz0123456789')
        clean = (i if i in allowed else '_' for i in username)
        gp = (i for i, _ in itertools.groupby(clean))
        result = ''.join(gp).strip('_')
        return result

    @staticmethod
    def normalize_email(email: str):
        email = email or ""
        try:
            email_name, domain_part = email.strip().rsplit("@", 1)
        except ValueError:
            pass
        else:
            email = email_name + "@" + domain_part.lower()
        return email