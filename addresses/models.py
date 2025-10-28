from django.db import models
from django.conf import settings

class Pincode(models.Model):
    """
    Minimal mapping table for pin code -> district/state/country
    You can populate this via fixtures or admin.
    """
    pincode = models.CharField(max_length=10, unique=True)
    district = models.CharField(max_length=128)
    state = models.CharField(max_length=128)
    country = models.CharField(max_length=128, default="India")

    def __str__(self):
        return f"{self.pincode} - {self.district}, {self.state}"

class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='addresses')
    flat_no = models.CharField(max_length=64)
    street = models.CharField(max_length=128)
    landmark = models.CharField(max_length=128, blank=True, null=True)
    area = models.CharField(max_length=128)
    pincode = models.CharField(max_length=10)
    district = models.CharField(max_length=128)
    state = models.CharField(max_length=128)
    country = models.CharField(max_length=64)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.flat_no}, {self.street}, {self.area} - {self.pincode}"

