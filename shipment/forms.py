from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import OrderForms


class RecipientInfo(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    phone_number = forms.CharField(required=True)
    address = forms.CharField(required=True)

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "phone_number", "address"]



class PackageInfo(UserCreationForm):
    package_name = forms.CharField(label='Package Name', max_length=100)
    package_weight = forms.DecimalField(label='Package Weight (kg)', max_digits=5, decimal_places=2)
    package_description = forms.CharField(label='Package Description', max_length=200)


    class Meta:
        model = User
        fields = ["package_name", "package_weight", "package_description"]

