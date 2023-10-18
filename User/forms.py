from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import CustomUser



class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    phone_number = forms.CharField(required=True)

    class Meta:
        model = CustomUser
        fields = ["first_name", "last_name", "username", "email", "phone_number", "password1", "password2"]



class UserUpdateForm(forms.Form):
    first_name = forms.CharField(max_length=100, required=False)
    last_name = forms.CharField(max_length=100, required=False)
    username = forms.CharField(max_length=100, required=False)
    email = forms.EmailField(required=False)
    phone_number = forms.CharField(max_length=15, required=False)
    password = forms.CharField(widget=forms.PasswordInput, required=False)


