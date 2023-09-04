from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="index"),
    path("blog", views.blog, name="blog"),
    path("about", views.about, name="about"),
    path("team", views.team, name="team"),
    path("contact", views.contact, name="contact"),
]