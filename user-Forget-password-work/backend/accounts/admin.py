# Admin configuration
from django.contrib import admin
from .models import User, OTPCode

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', )

@admin.register(OTPCode)
class OTPAdmin(admin.ModelAdmin):
    list_display = ('email', 'otp_code', 'expiry_time')
