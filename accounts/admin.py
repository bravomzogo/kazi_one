from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    # Define how the user model is displayed in the admin list
    list_display = ('username', 'email', 'first_name', 'last_name', 'facility', 'role', 'is_staff')
    
    # Add filters for these fields in the admin interface
    list_filter = ('facility', 'role', 'is_staff', 'is_superuser')
    
    # Group fields in the edit/add user form
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Professional info', {'fields': ('facility', 'role', 'department', 'phone_number')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    # Fields to include when adding a new user
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'email', 'first_name', 'last_name', 'facility', 'role'),
        }),
    )

# Register the CustomUser model with the CustomUserAdmin class
admin.site.register(CustomUser, CustomUserAdmin)