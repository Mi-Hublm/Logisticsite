from django.urls import path
from django.contrib.auth.decorators import login_required
from shipment import views

urlpatterns = [
    path("order", login_required(views.order), name="order"),
    path("package", login_required(views.package_info), name="package"),
]