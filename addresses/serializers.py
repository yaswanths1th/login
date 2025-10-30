from rest_framework import serializers
from .models import Address, Pincode

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = [
            "id", "user", "flat_no", "street", "landmark",
            "area", "pincode", "district", "state", "country", "created_at"
        ]
        read_only_fields = ["id", "created_at"]

    def validate(self, data):
        # If pincode is provided, try to auto-fill from Pincode table
        pincode = data.get("pincode")
        if pincode:
            try:
                pin_obj = Pincode.objects.get(pincode=pincode)
                data["district"] = data.get("district") or pin_obj.district
                data["state"] = data.get("state") or pin_obj.state
                data["country"] = data.get("country") or pin_obj.country
            except Pincode.DoesNotExist:
                # Do not raise here — we allow Geoapify fallback in view
                pass
        return data
