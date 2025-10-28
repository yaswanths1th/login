from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import AddressSerializer
from .utils import (
    connectDatabase, getAddressValidationRules, getAddressErrors,
    getLocationDetails, addressFieldValidation, insertAddress
)
from .models import Pincode

class LocationDetailsView(APIView):
    """
    GET ?pincode=xxxxx
    """
    def get(self, request):
        pincode = request.query_params.get("pincode")
        if not pincode:
            return Response({"error": "pincode param required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            loc = getLocationDetails(pincode)
            return Response({"success": True, "data": loc}, status=status.HTTP_200_OK)
        except ValueError:
            return Response({"success": False, "error": "pincode not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"success": False, "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class AddressCreateView(APIView):
    """
    POST: Create Address
    Expected JSON:
    { "user_id": int, "flat_no":"", "street":"", "landmark":"", "area":"", "pincode":"", "country":"", "state":"", "district":"" }
    """
    def post(self, request):
        data = request.data
        # Basic presence check
        required = ["user_id", "flat_no", "street", "area", "pincode"]
        for r in required:
            if r not in data:
                return Response({"success": False, "error": f"{r} required"}, status=status.HTTP_400_BAD_REQUEST)

        valid, error = addressFieldValidation(
            houseNo=data.get("flat_no", ""),
            street=data.get("street", ""),
            landmark=data.get("landmark", ""),
            area=data.get("area", ""),
            pinCode=data.get("pincode", ""),
        )
        if not valid:
            return Response({"success": False, "error": error}, status=status.HTTP_400_BAD_REQUEST)

        # If country/state/district not passed, derive from pincode
        country = data.get("country")
        state = data.get("state")
        district = data.get("district")
        if not (country and state and district):
            try:
                loc = getLocationDetails(data.get("pincode"))
                country = country or loc.get("country")
                state = state or loc.get("state")
                district = district or loc.get("district")
            except Exception as e:
                return Response({"success": False, "error": "Pincode lookup failed"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            address_obj = insertAddress(
                user_id=data.get("user_id"),
                flat_no=data.get("flat_no"),
                street=data.get("street"),
                landmark=data.get("landmark"),
                area=data.get("area"),
                pincode=data.get("pincode"),
                district=district,
                state=state,
                country=country,
            )
            serializer = AddressSerializer(address_obj)
            return Response({"success": True, "data": serializer.data}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"success": False, "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ValidationRulesView(APIView):
    def get(self, request):
        return Response({"success": True, "rules": getAddressValidationRules()})

class ValidationErrorsView(APIView):
    def get(self, request):
        return Response({"success": True, "errors": getAddressErrors()})

