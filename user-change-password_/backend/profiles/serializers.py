from rest_framework import serializers
from django.contrib.auth import password_validation

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_new_password(self, value):
        # Use Django's password validators
        password_validation.validate_password(value, self.context.get('user'))
        return value
