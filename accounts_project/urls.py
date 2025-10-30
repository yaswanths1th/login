from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    path("", lambda request: redirect("api/addresses/")),  # root -> /api/addresses/
    path("admin/", admin.site.urls),
    path("api/addresses/", include("addresses.urls")),
]
