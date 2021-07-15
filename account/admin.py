from django.contrib import admin
from .models import CustomUser
from django.contrib.auth.admin import UserAdmin
# Register your models here.
@admin.register(CustomUser)
class CustomADmin(UserAdmin):
    fieldsets=()
    filter_horizontal=()
    list_filter=()
    list_display=('email','username','login_date','is_active','is_admin')