from django.shortcuts import redirect
from django.utils import timezone
from django.db.models import Count
from datetime import timedelta
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Registration
from .serializers import RegistrationSerializer

class RegistrationListCreate(APIView):
    def get(self, request):
        regs = Registration.objects.order_by("-created_at")[:20]
        serializer = RegistrationSerializer(regs, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RegistrationStats(APIView):
    def get(self, request):
        now = timezone.now()
        start_of_today = now.replace(hour=0, minute=0, second=0, microsecond=0)
        start_of_week = start_of_today - timedelta(days=now.weekday())  # Monday
        today_count = Registration.objects.filter(created_at__gte=start_of_today).count()
        week_count = Registration.objects.filter(created_at__gte=start_of_week).count()
        total_count = Registration.objects.count()
        return Response({
            "today": today_count,
            "week": week_count,
            "total": total_count
        })
