from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse

def home(request):
    return HttpResponse("<h1>Welcome to the Backend Home Page</h1>")

urlpatterns = [
    path('', home),  # 👈 this handles http://127.0.0.1:8000/
    path('admin/', admin.site.urls),
    path('api/registrations/', include('registrations.urls')),
]
