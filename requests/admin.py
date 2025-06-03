from django.contrib import admin
from .models import DataRequest, Consent, DepartmentNotification

@admin.register(DataRequest)
class DataRequestAdmin(admin.ModelAdmin):
    # Display fields in list view
    list_display = ('id', 'patient', 'requester', 'hrio', 'status', 'created_at', 'expires_at')
    
    # Add filters
    list_filter = ('status', 'created_at', 'updated_at', 'expires_at')
    
    # Searchable fields
    search_fields = (
        'patient__patient_number', 
        'patient__first_name', 
        'patient__last_name',
        'requester__username',
        'hrio__username',
        'purpose'
    )
    
    # Fields to display in detail view (grouped)
    fieldsets = (
        ('Request Information', {
            'fields': ('requester', 'hrio', 'patient', 'purpose', 'status')
        }),
        ('Timing Information', {
            'fields': ('created_at', 'updated_at', 'expires_at'),
            'classes': ('collapse',)
        }),
    )
    
    # Read-only fields
    readonly_fields = ('created_at', 'updated_at')
    
    # Set default ordering
    ordering = ('-created_at',)

@admin.register(Consent)
class ConsentAdmin(admin.ModelAdmin):
    # Display fields in list view
    list_display = ('request', 'get_response_display', 'response_received_at', 'has_override')
    
    # Add filters
    list_filter = ('response', 'response_received_at')
    
    # Search through related request fields
    search_fields = (
        'request__patient__patient_number',
        'request__patient__first_name',
        'request__patient__last_name',
        'request__requester__username',
        'override_justification'
    )
    
    # Fields to display in detail view
    fieldsets = (
        ('Consent Information', {
            'fields': ('request', 'response', 'response_received_at')
        }),
        ('Override Information', {
            'fields': ('override_justification',),
            'classes': ('collapse',)
        }),
    )
    
    # Custom field to show if override exists
    def has_override(self, obj):
        return bool(obj.override_justification)
    has_override.boolean = True
    has_override.short_description = 'Override?'

@admin.register(DepartmentNotification)
class DepartmentNotificationAdmin(admin.ModelAdmin):
    # Display fields in list view
    list_display = ('request', 'hod', 'response', 'responded_at', 'is_responded')
    
    # Add filters
    list_filter = ('response', 'responded_at')
    
    # Search through related fields
    search_fields = (
        'request__patient__patient_number',
        'request__patient__first_name',
        'request__patient__last_name',
        'hod__username',
        'request__requester__username'
    )
    
    # Fields to display in detail view
    fieldsets = (
        ('Notification Information', {
            'fields': ('request', 'hod')
        }),
        ('Response Information', {
            'fields': ('response', 'responded_at'),
            'classes': ('collapse',)
        }),
    )
    
    # Custom field to show if response exists
    def is_responded(self, obj):
        return bool(obj.response)
    is_responded.boolean = True
    is_responded.short_description = 'Responded?'