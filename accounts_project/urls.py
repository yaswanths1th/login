from django.urls import path, include

urlpatterns = [
    path("api/addresses/", include("addresses.urls")),
    # other routes...
]

