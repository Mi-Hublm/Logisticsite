from django.shortcuts import render
from django.contrib import messages
import logging
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

def blog(request):

    try:    
        get_all_posts = Post.objects.all().order_by('-date')[:6]
        context = {
            'posts': get_all_posts
        }
        
    except Exception as e:
        logger.error("Faild to fetch data from database: %s", e)
        messages.error(request, "Check your internet connection and try again.")
        return render(request, "Logisticssite/blog.html")
    return render(request, "Logisticssite/blog.html", context)

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