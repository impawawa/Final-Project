from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

class RegisterForm(forms.Form):
    username = forms.CharField(max_length=150)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    def save(self):
        data = self.cleaned_data
        user = User.objects.create_user(
            username=data['username'],
            email=data['email'],
            password=data['password']
        )
        return user

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def authenticate_user(self):
        data = self.cleaned_data
        user = authenticate(username=data['username'], password=data['password'])
        return user
