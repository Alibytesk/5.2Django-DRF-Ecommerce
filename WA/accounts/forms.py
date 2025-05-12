from django import forms
from .validators import *

class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'username'}),
        max_length=255
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'password'})
    )

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username.isdigit():
            return PhoneValidator.phone_validate(phone=username)
        if '.' in username or '@' in username:
            email_name, domain_part = username.strip().rsplit("@", 1)
            if email_name and domain_part and '.' in domain_part:
                return username
            raise forms.ValidationError('invalid email')
        return username