from django.shortcuts import render, redirect
from django.contrib import messages
import logging
from django.core.paginator import Paginator
import requests
# from django.utils.logging import getLogger
# from django.http import HttpResponse
# from rest_framework.decorators import api_view
# from rest_framework.response import Response
from . models import Post, Team

logger = logging.getLogger(__name__)

# Create your views here.


def home(request):
    get_all_team = Team.objects.all()[:3]

    get_all_posts = Post.objects.all().order_by('-date')[:3]

    context = {
        'teams': get_all_team,

        'posts': get_all_posts
    }
    return render(request,"Logisticssite/index.html", context)


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
            # Registration was successful
            return redirect('index')  # Redirect to a success page in Django
        else:
            # Registration failed
            error_message = response.json().get('message', 'Registration failed')
            return render(request, 'Logisticssite/register.html', {'error_message': error_message})

    return render(request, "Logisticssite/register.html")

def login(request):
    if request.method == 'POST':
        # Get user login data from the form
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Construct the data to send to the Flask API
        data = {
            'username': username,
            'password': password
        }

        # Make an HTTP POST request to the Flask API's authentication endpoint
        response = requests.post('http://127.0.0.1:5000/api/authenticate', json=data)

        # Check the response from the Flask API
        if response.status_code == 200:
            # Authentication was successful
            access_token = response.json().get('access_token')
            # Store the access token or perform additional actions
            return redirect('blog')  # Redirect to a dashboard page in Django
        else:
            # Authentication failed
            error_message = response.json().get('message', 'Authentication failed')
            return render(request, 'Logisticssite/login.html', {'error_message': error_message})

    return render(request, "Logisticssite/login.html")



def blog(request):

    # try:    
    get_all_posts = Post.objects.all().order_by('-date')
    paginator = Paginator(get_all_posts, 3)
    page = request.GET.get('page')
    page_obj = paginator.get_page(page)
    context = {
            'posts': page_obj,
        }
        
    # except Exception as e:
    #     logger.error("Faild to fetch data from database: %s", e)
    #     messages.error(request, "Check your internet connection and try again.")
    #     return render(request, "Logisticssite/blog.html")
    return render(request, "Logisticssite/blog.html", context)


def blog_single(request, pk):
    get_post = Post.objects.get(pk=pk)
    context = {
        'post': get_post
    }
    return render(request, "Logisticssite/blog_single.html", context)


def about(request):
    return render(request, "Logisticssite/about.html")

def team(request):
    get_all_team = Team.objects.all()

    context = {
        'teams': get_all_team
    }
    return render(request, "Logisticssite/team.html", context)

def contact(request):
    return render(request, "Logisticssite/contact.html")

def protection(request):
    return render(request, "Logisticssite/protection.html")


def services(request):
    pass


def service_single(request):
    pass

def errorpage(request):
    pass

def project(request):
    pass


def project_single(request):
    pass