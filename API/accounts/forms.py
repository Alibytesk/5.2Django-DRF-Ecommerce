from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from accounts.models import User

class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder':'password'})
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder':'confirmation password'})
    )
    class Meta:
        model = User
        fields = ('phone',)

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password2 != password1 and password2 and password1:
            raise ValueError('password does not match')
        return cleaned_data

    def save(self, commit=False):
        user = super().save(commit=True)
        password = self.cleaned_data.get('password1')
        user.set_password(password)
        user.save()


class UserChangeForm(forms.ModelForm):

    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('phone', 'username', 'email', 'password', 'is_active')