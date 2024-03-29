from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="index"),
    # path("logout", views.logout, name="logout"),
    #path("user_dashboard", views.user_dash, name="user_dash"),
    path("blog", views.blog, name="blog"),
    path("about", views.about, name="about"),
    path("team", views.team, name="team"),
    path("contact", views.contact, name="contact"),
    path("protection", views.protection, name="protection"),
    path("bog_single<int:pk>", views.blog_single, name="single"),
    path("services", views.services, name="single"),
    path("service_single<int:pk>", views.service_single, name="service_single"),
    path("project", views.project, name="single"),
    path("project_single<int:pk>", views.project_single, name="project_single"),
    path("errorpage", views.errorpage, name="404"),
]