from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include('django.contrib.auth.urls')),
    # path('', include('social_django.urls', namespace='social')),
    path("", include("Logisticssite.urls")),
    path("", include("shipment.urls")),
    path("", include("User.urls")),
    path("", include("Payment.urls")),
]