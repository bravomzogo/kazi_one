from django.db import models
from django.core.validators import MinLengthValidator
from accounts.models import CustomUser

class Patient(models.Model):
    STATUS_CHOICES = [
        ('NORMAL', 'Normal'),
        ('CHRONIC', 'Chronic'),
        ('CRITICAL', 'Critical'),
    ]
    
    patient_number = models.CharField(
        max_length=20, 
        unique=True,
        validators=[MinLengthValidator(10)]
    )
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='NORMAL')
    phone_number = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    @property
    def current_department(self):
        latest_record = self.records.order_by('-created_at').first()
        return latest_record.department if latest_record else 'Unknown'
    
    def __str__(self):
        return f"{self.patient_number} - {self.first_name} {self.last_name}"

class PatientRecord(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='records')
    diagnosis = models.TextField()
    treatment = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    department = models.CharField(max_length=100)
    created_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    data_hash = models.CharField(max_length=64, blank=True)
    
    def __str__(self):
        return f"Record for {self.patient} - {self.diagnosis[:50]}"
    
    def save(self, *args, **kwargs):
        import hashlib
        data_str = f"{self.diagnosis}{self.treatment}{self.notes}{self.department}"
        self.data_hash = hashlib.sha256(data_str.encode()).hexdigest()
        super().save(*args, **kwargs)