from django.urls import path
from .views import AddressListCreateView, get_location_by_pincode

urlpatterns = [
    path("", AddressListCreateView.as_view(), name="address-list-create"),  # POST to /api/addresses/
    path("pincode/", get_location_by_pincode, name="get-location-by-pincode"),  # GET /api/addresses/pincode/?pincode=110001
]
