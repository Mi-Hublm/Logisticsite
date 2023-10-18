from django.urls import path
from django.contrib.auth.decorators import login_required
from shipment import views

urlpatterns = [
    path('order', views.recipient_info, name='order'),
    path('package', views.package_info, name='package'),
    path('confirm_order', views.confirm_order, name='confirm_order'),
    path('submit_order', views.submit_order, name='submit_order'),
    path('order_success', views.order_success, name='order_success'),
]