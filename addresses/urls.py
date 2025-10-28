from django.urls import path
from .views import LocationDetailsView, AddressCreateView, ValidationRulesView, ValidationErrorsView

urlpatterns = [
    path("location/", LocationDetailsView.as_view(), name="address-location"),
    path("", AddressCreateView.as_view(), name="address-create"),
    path("rules/", ValidationRulesView.as_view(), name="address-rules"),
    path("errors/", ValidationErrorsView.as_view(), name="address-errors"),
]

