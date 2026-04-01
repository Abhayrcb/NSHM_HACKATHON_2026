from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin


@admin.register(User)
class UserAdmin(UserAdmin):
    list_display  = ['email','role','username','first_name','last_name','mobile']
    fieldsets = [
        ('User Credentials', {'fields': ['email', 'password']}),
        ('Personal Info', {'fields': ['username', 'first_name', 'last_name','role','mobile']}),
        ('Permissions', {'fields': ['is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions']}),
    ]
    add_fieldsets = [
        ('User Credentials', {'fields': ['email', 'password1', 'password2']}),
        ('Personal Info', {'fields': ['username', 'first_name', 'last_name','role','mobile']}),
    ]
    
    
    search_fields = ['email','username']
    ordering = ['email']