# Models for users/OTP
from django.db import models

class User(models.Model):
    """
    Simple user model for demo:
    - email is unique
    - password is the hashed password (Django's hashing utilities used in views)
    """
    email = models.EmailField(unique=True, max_length=255)
    password = models.CharField(max_length=255)  # hashed

    def __str__(self):
        return self.email

class OTPCode(models.Model):
    """
    Stores OTP codes temporarily
    """
    email = models.EmailField(max_length=255)
    otp_code = models.CharField(max_length=6)
    expiry_time = models.DateTimeField()

    def __str__(self):
        return f"{self.email} - {self.otp_code}"
