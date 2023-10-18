from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from rest_framework.authtoken.models import Token
from django.contrib.auth import login
import requests
import json
from .forms import RegisterForm, UserUpdateForm
from shipment.models import Order  



def sign_up(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('profile')
    else:
        form=RegisterForm()
    return render(request, 'registration/sign_up.html', {"form": form})

@login_required
def user_dash(request):

    return render(request, "user_dash.html")


@login_required
def profile(request):
    if request.method == "POST":
        form = UserUpdateForm(request.POST)
        if form.is_valid():
            user = request.user
            user.first_name = form.cleaned_data.get('first_name', user.first_name)
            user.last_name = form.cleaned_data.get('last_name', user.last_name)
            user.username = form.cleaned_data.get('username', user.username)
            user.email = form.cleaned_data.get('email', user.email)
            # user.phone_number = form.cleaned_data.get('phone_number', user.phone_number)

            password = form.cleaned_data.get('password')
            if password:
                user.set_password(password)

            user.save()

    else:
        # Initialize the form with the user's current data
        initial_data = {
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'username': request.user.username,
            'email': request.user.email,
            # 'phone_number': request.user.phone_number,
        }
        form = UserUpdateForm(initial=initial_data)

    return render(request, "profile.html", {'form': form})
