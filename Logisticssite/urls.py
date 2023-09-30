from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="index"),
    path("register", views.register, name="register"),
    path("login", views.login, name="login"),
    path("blog", views.blog, name="blog"),
    path("about", views.about, name="about"),
    path("team", views.team, name="team"),
    path("contact", views.contact, name="contact"),
    path("protection", views.protection, name="protection"),
    path("bog_single<int:pk>", views.blog_single, name="single"),
    path("services", views.services, name="single"),
    path("service_single<int:pk>", views.service_single, name="single"),
    path("project", views.project, name="single"),
    path("project_single<int:pk>", views.project_single, name="single"),
    path("errorpage", views.errorpage, name="single"),
]