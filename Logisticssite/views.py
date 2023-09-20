from django.shortcuts import render
# from django.http import HttpResponse
# from rest_framework.decorators import api_view
# from rest_framework.response import Response
from . models import Post, Team

# Create your views here.


def home(request):
    return render(request,"Logisticssite/index.html")

def blog(request):
    get_all_posts = Post.objects.all().order_by('-date')[:6]
    context = {
        'posts': get_all_posts
    }
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