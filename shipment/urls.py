from django.urls import path
from shipment import views

urlpatterns = [
    path("new_order", views.new_order, name="order"),
]