# Django model definitions
from django.db import models

class UserProfile(models.Model):
    name = models.CharField(max_length=200, default="MAHENDRA")
    phone = models.CharField(max_length=20, blank=True, default="7845637474")
    email = models.EmailField(blank=True, default="mahi@gmail.com")
    house = models.CharField(max_length=200, blank=True, default="3rd Floor")
    street = models.CharField(max_length=200, blank=True, default="Bank Street")
    landmark = models.CharField(max_length=200, blank=True, default="Near Hdfc")
    area = models.CharField(max_length=200, blank=True, default="Koti")
    district = models.CharField(max_length=200, blank=True, default="Rangareddy")
    state = models.CharField(max_length=200, blank=True, default="Telangana")
    country = models.CharField(max_length=100, blank=True, default="India")
    pincode = models.CharField(max_length=20, blank=True, default="500001")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.email})"
