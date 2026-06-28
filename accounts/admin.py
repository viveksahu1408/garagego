from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    model = User
    fieldsets = UserAdmin.fieldsets + (
        ('Custom Roles & Info', {'fields': ('is_customer', ('is_mechanic', 'is_admin_staff'), 'phone_number', 'city')}),
    )

admin.site.register(User, CustomUserAdmin)