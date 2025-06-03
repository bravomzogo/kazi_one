from django.contrib import admin
from .models import Patient, PatientRecord

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    # Display fields in list view
    list_display = ('patient_number', 'first_name', 'last_name', 'date_of_birth', 'status', 'current_department', 'created_at')
    
    # Add filters
    list_filter = ('status', 'created_at', 'updated_at')
    
    # Searchable fields
    search_fields = ('patient_number', 'first_name', 'last_name', 'phone_number', 'email')
    
    # Fields to display in detail view (grouped)
    fieldsets = (
        ('Basic Information', {
            'fields': ('patient_number', 'first_name', 'last_name', 'date_of_birth', 'status')
        }),
        ('Contact Information', {
            'fields': ('phone_number', 'email')
        }),
        ('Metadata', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    # Read-only fields
    readonly_fields = ('created_at', 'updated_at', 'current_department')
    
    # Set default ordering
    ordering = ('-created_at',)

@admin.register(PatientRecord)
class PatientRecordAdmin(admin.ModelAdmin):
    # Display fields in list view
    list_display = ('patient', 'department', 'diagnosis_short', 'created_at', 'created_by')
    
    # Add filters
    list_filter = ('department', 'created_at', 'updated_at')
    
    # Searchable fields
    search_fields = ('patient__patient_number', 'patient__first_name', 'patient__last_name', 'diagnosis', 'treatment')
    
    # Fields to display in detail view (grouped)
    fieldsets = (
        ('Record Information', {
            'fields': ('patient', 'department', 'diagnosis', 'treatment', 'notes')
        }),
        ('Metadata', {
            'fields': ('created_by', 'data_hash', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    # Read-only fields
    readonly_fields = ('created_at', 'updated_at', 'data_hash')
    
    # Set default ordering
    ordering = ('-created_at',)
    
    # Custom method to display shortened diagnosis
    def diagnosis_short(self, obj):
        return obj.diagnosis[:50] + '...' if len(obj.diagnosis) > 50 else obj.diagnosis
    diagnosis_short.short_description = 'Diagnosis'