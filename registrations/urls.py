from django.urls import path
from .views import RegistrationListCreate, RegistrationStats

urlpatterns = [
    path("", RegistrationListCreate.as_view(), name="registrations-list"),
    path("stats/", RegistrationStats.as_view(), name="registrations-stats"),
    
]
 
