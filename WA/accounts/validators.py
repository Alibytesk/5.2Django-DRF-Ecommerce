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
    