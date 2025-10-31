# Django views
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import UserProfile
from .serializers import UserProfileSerializer

class ProfileAPIView(APIView):
    """
    GET: return the single user profile (create with dummy data if none).
    PUT: update the profile.
    """

    def get_profile(self):
        # Get the first profile, or create one with default dummy data.
        # Using get_or_create ensures there is always a profile to return.
        obj, created = UserProfile.objects.get_or_create(pk=1, defaults={
            # defaults are already provided in model fields, but explicit is ok:
            'name': 'MAHENDRA',
            'phone': '7845637474',
            'email': 'mahi@gmail.com',
            'house': '3rd Floor',
            'street': 'Bank Street',
            'landmark': 'Near Hdfc',
            'area': 'Koti',
            'district': 'Rangareddy',
            'state': 'Telangana',
            'country': 'India',
            'pincode': '500001'
        })
        return obj

    def get(self, request, format=None):
        profile = self.get_profile()
        serializer = UserProfileSerializer(profile)
        return Response(serializer.data)

    def put(self, request, format=None):
        profile = self.get_profile()
        serializer = UserProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
