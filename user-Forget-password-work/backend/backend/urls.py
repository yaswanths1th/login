from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse

# Simple home view
def home(request):
    return JsonResponse({"message": "Django backend is running successfully!"})

urlpatterns = [
    path('', home),  # 👈 This handles http://127.0.0.1:8000/
    path('admin/', admin.site.urls),
    path('api/', include('accounts.urls')),  # Your app routes
]
