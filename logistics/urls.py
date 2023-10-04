from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', include('social_django.urls', namespace='social')),
    path("", include("Logisticssite.urls")),
    path("shipment/", include("shipment.urls")),
    path("User/", include("User.urls")),
    path("Payment/", include("Payment.urls")),
]
