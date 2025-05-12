from django import forms

class PhoneValidator:

    @staticmethod
    def phone_validate(phone: str):
        errors = list()
        if not phone.isdigit():
            errors.append('phone can not be character')
        if not phone.startswith('09'):
            errors.append('phone should start with 09 number')
        if not len(phone) == 11:
            errors.append('phone must be 11 numbers')
        if errors:
            raise forms.ValidationError(errors)
        return phone
    
class PasswordValidation:

    @staticmethod
    def password_validator(password1):
        errors, allowed_char = list(), '!@#$%^&*'
        if not password1:
            raise ValueError('users must have a strong password')
        else:
            if not any(i.isdigit() for i in password1):
                errors.append('password must contain at least one number')
            if not any(i in allowed_char for i in password1):
                errors.append('password must contain at least one special character')
            if not any(i.isupper() for i in password1):
                errors.append('password must contain at least one uppercase character')
            if not any(i.islower() for i in password1):
                errors.append('password must contain at least one lowercase character')
            if len(password1) < 8:
                errors.append('password must be at least 8 character')
            if not errors:
                return password1
            else:
                raise forms.ValidationError(errors)
