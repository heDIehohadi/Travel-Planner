from django.contrib import admin
from apps.accounts.models import User, OTPRequest
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display=['phone_number','is_active','date_joined','is_staff','is_phone_verified']
    search_fields=['phone_number','first_name','last_name']
    list_filter=['date_joined']
    ordering=['phone_number','date_joined']
@admin.register(OTPRequest)
class OTPrequestAdmin(admin.ModelAdmin):
     list_display=['phone_number','otp_code','is_used','attempts','created_at','expires_at']