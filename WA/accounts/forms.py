from django import forms
from django.core import validators
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
    
class RegisterForm(forms.Form):
    phone = forms.CharField(
        validators=(PhoneValidator.phone_validate,),
        widget=forms.NumberInput(attrs={'placeholder':'Phone Number', 'class':'form-control'})
    )

class OtpcheckForm(forms.Form):

    code = forms.CharField(
        validators=(validators.MaxLengthValidator(4),),
        widget=forms.NumberInput(attrs={'class':'form-control', 'placeholder':'code'})
    )
    username = forms.CharField(
        validators=(validators.MaxLengthValidator(40), validators.MinLengthValidator(4),),
        widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'username'})
    )
    email = forms.EmailField(
        validators=(validators.EmailValidator,),
        widget=forms.EmailInput(attrs={'class':'form-control', 'placeholder':'Email'})
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Password'})
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Confirmation Password'})
    )

    def clean_password1(self):
        return PasswordValidation.password_validator(self.cleaned_data['password1'])


class ChangePasswordForm(forms.Form):

    current_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'your current password',
            'class': 'form-control',
        })
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'new password',
            'class': 'form-control',
        })
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'confirmation password',
            'class': 'form-control',
        })
    )

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        return PasswordValidation.password_validator(password1=password1)
    

class EmailVerificationForm(forms.Form):
    code = forms.CharField(
        validators=(validators.MaxLengthValidator(6),validators.MinLengthValidator(6),),
        widget=forms.NumberInput(attrs={
            'placeholder': 'enter code',
            'class': 'form-control',
        })
    )


class EmailQueueAuthForm(forms.Form):
    email = forms.CharField(
        validators=(validators.EmailValidator,),
        widget=forms.EmailInput(attrs={'placeholder':'Your Email', 'class': 'form-control'}),
        max_length=255,
    )