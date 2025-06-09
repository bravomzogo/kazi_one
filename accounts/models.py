from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError

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
        ('RESEARCHER', 'Researcher'),
    ]
    
    facility = models.CharField(max_length=50, choices=FACILITY_CHOICES, blank=True, null=True) 
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, null=True, blank=True)
    department = models.CharField(max_length=100, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    
    def clean(self):
        if self.role == 'HOD' and not self.department:
            raise ValidationError("Head of Department must have a department assigned")
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.get_full_name()} ({self.get_role_display()})"

class ResearcherProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='researcher_profile')
    company = models.CharField(max_length=100)
    data_sought = models.TextField()
    hr_document = models.FileField(upload_to='hr_documents/')
    
    def __str__(self):
        return f"Profile for {self.user.username}"