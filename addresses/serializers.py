from rest_framework import serializers
from .models import Address

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = [
            "id", "user", "flat_no", "street", "landmark",
            "area", "pincode", "district", "state", "country", "created_at"
        ]
        read_only_fields = ["id", "created_at"]

