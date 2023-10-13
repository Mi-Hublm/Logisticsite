from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from rest_framework.authtoken.models import Token
from django.contrib.auth import login
import requests
import json
from .forms import RegisterForm


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
    return render(request, "profile.html")
