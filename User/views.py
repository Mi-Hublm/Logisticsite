from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from rest_framework.authtoken.models import Token
from django.contrib.auth import login
import requests
import json



def register(request):
    if request.method == 'POST':
        # Get user registration data from the form
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')

        # Construct the data to send to the Flask API
        data = {
            'username': username,
            'email': email,
            'password': password
        }

        # Make a POST request to the Flask API's registration endpoint
        response = requests.post('http://127.0.0.1:5000/api/register', json=data)

        # Check the response from the Flask API
        if response.status_code == 201:
            # Registration was successful in the Flask API

            try:
                # Attempt to parse the JSON response for the token
                token_data = response.json()
                access_token = token_data.get('access_token')

                # Print the token to the terminal
                print(f'Access Token: {access_token}')
            except json.JSONDecodeError as e:
                # Handle JSON decoding error (e.g., empty response)
                access_token = None

            # If a token was obtained, store it in the session for future API requests
            if access_token:
                request.session['access_token'] = access_token

                # Redirect to the login page with a success message (optional)
                return redirect('login')

        else:
            try:
                # Attempt to parse the JSON response
                error_message = response.json().get('message', 'Registration failed')
            except json.JSONDecodeError as e:
                # Handle JSON decoding error (e.g., empty response)
                error_message = 'Error: Invalid response from the API'

            return render(request, 'register.html', {'error_message': error_message})

    return render(request, "register.html")


def user_login(request):
    authentication_message = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        data = {
            'username': username,
            'password': password
        }

        response = requests.post('http://127.0.0.1:5000/api/login', json=data)

        if response.status_code == 200:
            response_data = response.json()
            access_token = response_data.get('access_token')

            if access_token:
                # Store the access token in the session (if needed)
                request.session['access_token'] = access_token
                
                # Redirect to the user dashboard or another appropriate page
                return redirect('userdash')
            else:
                authentication_message = 'Error: Access token not found in the API response'
        else:
            try:
                error_message = response.json().get('message', 'Authentication failed')
                authentication_message = f'Authentication failed: {error_message}'
            except json.JSONDecodeError as e:
                authentication_message = 'Error: Invalid response from the API'

    return render(request, 'login.html', {'authentication_message': authentication_message})



@login_required
def user_dash(request):
    return render(request, "user_dash.html")


@login_required
def profile(request):
    return render(request, "profile.html")
