from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Address, Pincode
from .serializers import AddressSerializer
import requests
from django.contrib.auth import get_user_model

User = get_user_model()

# 🔹 Geoapify API key
GEOAPIFY_KEY = "cfbde6e6513242f68afce4e67a6595a3"


# ==========================================================
# 🔹 API 1: Get location info from pincode (Geoapify)
# ==========================================================
@api_view(["GET"])
def get_location_by_pincode(request):
    pincode = request.GET.get("pincode")
    if not pincode:
        return Response(
            {"success": False, "error": "Pincode is required"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    url = f"https://api.geoapify.com/v1/geocode/search?postcode={pincode}&apiKey={GEOAPIFY_KEY}"
    try:
        res = requests.get(url, timeout=10)
        res.raise_for_status()
        data = res.json()
        results = data.get("features") or data.get("results") or []
        if not results:
            return Response(
                {"success": False, "error": "No data found for this PIN code"},
                status=status.HTTP_404_NOT_FOUND,
            )

        props = results[0].get("properties") if isinstance(results[0], dict) else results[0]
        return Response(
            {
                "success": True,
                "data": {
                    "country": props.get("country", ""),
                    "state": props.get("state", "") or props.get("region", ""),
                    "district": props.get("county")
                    or props.get("city")
                    or props.get("district", ""),
                },
            },
            status=status.HTTP_200_OK,
        )
    except requests.exceptions.RequestException as e:
        return Response(
            {"success": False, "error": f"Geoapify error: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


# ==========================================================
# 🔹 API 2: Address List + Create (Auto-link user if logged in)
# ==========================================================
class AddressListCreateView(APIView):
    """
    GET -> list all addresses
    POST -> create a new address (auto-assigns logged-in user)
    """

    permission_classes = []

    def get(self, request):
        if request.user.is_authenticated:
            addresses = Address.objects.filter(user=request.user)
        else:
            addresses = Address.objects.all()  # public/test view
        serializer = AddressSerializer(addresses, many=True)
        return Response(
            {"success": True, "data": serializer.data},
            status=status.HTTP_200_OK,
        )

    def post(self, request):
        data = request.data.copy()

        # ✅ Automatically link the logged-in user (if any)
        if request.user.is_authenticated:
            data["user"] = request.user.id
        else:
            data["user"] = None  # guest/test mode

        # Validate required fields
        required_fields = ["flat_no", "street", "area", "pincode"]
        for field in required_fields:
            if not data.get(field):
                return Response(
                    {"success": False, "error": f"{field} is required"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        # 🔹 Auto-fill district/state/country if missing
        pincode = data.get("pincode")
        if pincode and not (data.get("district") and data.get("state") and data.get("country")):
            try:
                pin_obj = Pincode.objects.get(pincode=pincode)
                data["district"] = data.get("district") or pin_obj.district
                data["state"] = data.get("state") or pin_obj.state
                data["country"] = data.get("country") or pin_obj.country
            except Pincode.DoesNotExist:
                try:
                    url = f"https://api.geoapify.com/v1/geocode/search?postcode={pincode}&apiKey={GEOAPIFY_KEY}"
                    res = requests.get(url, timeout=10)
                    res.raise_for_status()
                    geo_data = res.json()
                    results = geo_data.get("features") or geo_data.get("results") or []
                    if results:
                        props = results[0].get("properties") if isinstance(results[0], dict) else results[0]
                        data["country"] = data.get("country") or props.get("country", "")
                        data["state"] = data.get("state") or props.get("state") or props.get("region", "")
                        data["district"] = (
                            data.get("district")
                            or props.get("county")
                            or props.get("city")
                            or props.get("district", "")
                        )
                except requests.exceptions.RequestException:
                    return Response(
                        {"success": False, "error": "Pincode lookup failed"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

        # 🔹 Save address
        serializer = AddressSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "success": True,
                    "message": "✅ Address saved successfully!",
                    "data": serializer.data,
                },
                status=status.HTTP_201_CREATED,
            )

        return Response(
            {"success": False, "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )
