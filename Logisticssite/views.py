from django.shortcuts import render
from django.contrib import messages
import logging
from django.core.paginator import Paginator
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