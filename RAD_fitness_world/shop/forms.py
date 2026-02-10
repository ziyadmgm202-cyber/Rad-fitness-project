from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.help_text = None


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'enter username', 'class': 'form-control'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'placeholder': 'enter password', 'class': 'form-control', 'id': 'password-field'})
    )