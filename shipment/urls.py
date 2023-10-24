from django.urls import path
from django.contrib.auth.decorators import login_required
from shipment import views

urlpatterns = [
    path("new_order", views.new_order, name="order"),
    path("new_orders/", views.create_new_shipment, name="create"),
    path('cancel/orders/<str:id>/', views.cancel_shipment, name='cancel'),
    path('activate/orders/<str:id>/', views.activate_cancelled_shipment, name='activate'),
    path('inactive/orders/', views.inactivate_shipments, name='view_inactivate'),
    path('update/', views.update_shipment, name='update'),
    path("order", login_required(views.order), name="order"),
    path("package", login_required(views.package_info), name="package"),
]