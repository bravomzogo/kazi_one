from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    FACILITY_CHOICES = [
        ('FAC1', 'Main Hospital'),
        ('FAC2', 'Regional Clinic'),
    ]
    
    ROLE_CHOICES = [
        ('HRIO', 'Health Records Information Officer'),
        ('DOCTOR', 'Doctor'),
        ('NURSE', 'Nurse'),
        ('PHARMACIST', 'Pharmacist'),
        ('ICT', 'ICT Staff'),
        ('HOD', 'Head of Department'),
        ('ADMIN', 'System Administrator'),
        ('AUDITOR', 'Auditor'),
    ]
    
    facility = models.CharField(max_length=50, choices=FACILITY_CHOICES)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    department = models.CharField(max_length=100, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    
    def __str__(self):
        return f"{self.get_full_name()} ({self.get_role_display()})"