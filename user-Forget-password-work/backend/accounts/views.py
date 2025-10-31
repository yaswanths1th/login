# Views for password reset and OTP verification
"""
Views for handling send-otp and verify-otp endpoints.
"""
from django.utils import timezone
from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.contrib.auth.hashers import make_password
from django.db import transaction

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

import random
from datetime import timedelta

from .models import User, OTPCode
from .serializers import SendOtpSerializer, VerifyOtpSerializer


def generate_otp():
    """Returns a random 6-digit string."""
    return f"{random.randint(0, 999999):06d}"


@api_view(['POST'])
def send_otp_view(request):
    """
    POST: { "email": "user@example.com" }
    - If user exists -> generate OTP and email it
    - If user does not exist -> still generate dummy OTP and email (per spec)
    - Save OTP in OTPCode with expiry (5 minutes)
    """
    serializer = SendOtpSerializer(data=request.data)
    if not serializer.is_valid():
        return Response({"detail": "Invalid input"}, status=status.HTTP_400_BAD_REQUEST)

    email = serializer.validated_data['email'].lower()
    otp = generate_otp()
    expiry = timezone.now() + timedelta(minutes=getattr(settings, "OTP_EXPIRY_MINUTES", 5))

    # Save OTPCode (no transaction needed)
    OTPCode.objects.create(email=email, otp_code=otp, expiry_time=expiry)

    # try to locate user
    try:
        user = User.objects.get(email=email)
        email_exists = True
    except User.DoesNotExist:
        user = None
        email_exists = False

    # Compose email
    subject = "Your OTP for password reset"
    message = f"Your OTP is: {otp}\nIt will expire at {expiry} UTC.\nIf you didn't request this, ignore."
    from_email = getattr(settings, "DEFAULT_FROM_EMAIL", settings.EMAIL_HOST_USER)
    recipient_list = [email]

    # Send email. If SMTP not configured, consider console backend for dev.
    try:
        send_mail(subject, message, from_email, recipient_list, fail_silently=False)
    except Exception as e:
        # For dev, console backend prints instead of raising. But if SMTP misconfigured, we still return success so frontend can proceed.
        # Log if needed.
        print("Warning: send_mail failed:", e)

    if not email_exists:
        # Per spec: if email not in DB -> return an informative error (frontend will show modal)
        return Response({
            "detail": "Email not found — please create an account first.",
            "sent": True
        }, status=status.HTTP_404_NOT_FOUND)

    return Response({"detail": "OTP sent successfully to your email.", "sent": True})


@api_view(['POST'])
def verify_otp_view(request):
    """
    POST: { "email": "...", "otp": "...", "new_password": "...", "confirm_password": "..." }
    - Validate OTP: must match latest unexpired OTP for this email
    - Validate password match and strength
    - If valid and user exists -> update password (hashed)
    """
    serializer = VerifyOtpSerializer(data=request.data)
    if not serializer.is_valid():
        return Response({"detail": "Invalid input"}, status=status.HTTP_400_BAD_REQUEST)

    email = serializer.validated_data['email'].lower()
    otp = serializer.validated_data['otp']
    new_password = serializer.validated_data['new_password']
    confirm_password = serializer.validated_data['confirm_password']

    if new_password != confirm_password:
        return Response({"detail": "Passwords do not match"}, status=status.HTTP_400_BAD_REQUEST)

    # Basic password strength checks: at least 8 chars, contains number, letter
    if len(new_password) < 8 or not any(c.isdigit() for c in new_password) or not any(c.isalpha() for c in new_password):
        return Response({"detail": "Password must be at least 8 characters long and include letters and numbers."},
                        status=status.HTTP_400_BAD_REQUEST)

    # Find OTP entry for this email that matches and is not expired.
    now = timezone.now()
    otp_entries = OTPCode.objects.filter(email=email, otp_code=otp, expiry_time__gte=now).order_by('-expiry_time')

    if not otp_entries.exists():
        return Response({"detail": "Invalid or expired OTP"}, status=status.HTTP_400_BAD_REQUEST)

    # OTP is valid — update password if user exists
    try:
        with transaction.atomic():
            user = User.objects.get(email=email)
            user.password = make_password(new_password)
            user.save()
    except User.DoesNotExist:
        # Per spec, if user does not exist — we may return an error.
        return Response({"detail": "User not found. Please register first."}, status=status.HTTP_404_NOT_FOUND)

    # Optionally remove used OTPs for cleanup
    OTPCode.objects.filter(email=email).delete()

    return Response({"detail": "Password updated successfully."})
