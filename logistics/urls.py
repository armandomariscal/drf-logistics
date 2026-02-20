from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("apps.orders.presentation.urls")),
    path("api/", include("apps.payments.presentation.urls")),
]
