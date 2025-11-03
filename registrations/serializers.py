from rest_framework import serializers
from .models import Registration

class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Registration
        fields = ["id", "name", "email", "status", "created_at"]
 
