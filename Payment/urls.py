from django.urls import path
from Payment import views

urlpatterns = [
    path("", views.payment, name="payment"),
]  