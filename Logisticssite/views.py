from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


def home(request):
    return render(request,"Logisticssite/index.html")

def blog(request):
    return render(request, "Logisticssite/blog.html")

def about(request):
    return render(request, "Logisticssite/about.html")

def team(request):
    return render(request, "Logisticssite/team.html")

def contact(request):
    return render(request, "Logisticssite/contact.html")

def protection(request):
    return render(request, "Logisticssite/protection.html")