from django.db import models
from django.utils import timezone
from accounts.models import CustomUser
from patients.models import Patient

class DataRequest(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('DENIED', 'Denied'),
        ('EXPIRED', 'Expired'),
    ]
    
    requester = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='requests_made')
    hrio = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='requests_handled')
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    purpose = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    expires_at = models.DateTimeField()

    
    def __str__(self):
        return f"Request #{self.id} for {self.patient} by {self.requester}"
    
    def save(self, *args, **kwargs):
        if not self.pk:
            self.expires_at = timezone.now() + timezone.timedelta(minutes=2)
        super().save(*args, **kwargs)

class Consent(models.Model):
    RESPONSE_CHOICES = [
        ('PENDING', 'Pending'),
        ('GRANTED', 'Granted'),
        ('DENIED', 'Denied'),
        ('OVERRIDDEN', 'Overridden'),
    ]
    
    request = models.OneToOneField(
        DataRequest, 
        on_delete=models.CASCADE,
        primary_key=True  # Makes request_id the primary key
    )
    response = models.CharField(max_length=10, choices=RESPONSE_CHOICES, default='PENDING')
    response_received_at = models.DateTimeField(blank=True, null=True)
    override_justification = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"Consent for {self.request}"

class DepartmentNotification(models.Model):
    request = models.ForeignKey(DataRequest, on_delete=models.CASCADE)
    hod = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    response = models.CharField(max_length=10, blank=True, null=True)
    responded_at = models.DateTimeField(blank=True, null=True)
    
    def __str__(self):
        return f"Notification to {self.hod} about {self.request}"