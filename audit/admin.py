from django.contrib import admin
from .models import AuditLog

@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    # Display these fields in the list view
    list_display = ('timestamp', 'user', 'get_action_display', 'patient', 'ip_address')
    
    # Add filters for these fields
    list_filter = ('action', 'timestamp', 'user')
    
    # Make these fields searchable
    search_fields = ('user__username', 'description', 'patient__name', 'ip_address')
    
    # Fields to display in the detail view (grouped)
    fieldsets = (
        ('Action Information', {
            'fields': ('user', 'action', 'description', 'timestamp', 'ip_address')
        }),
        ('Related Objects', {
            'fields': ('patient', 'request'),
            'classes': ('collapse',)  # Makes this section collapsible
        }),
    )
    
    # Make the timestamp read-only in the admin
    readonly_fields = ('timestamp',)
    
    # Set default ordering (same as model's Meta)
    ordering = ('-timestamp',)