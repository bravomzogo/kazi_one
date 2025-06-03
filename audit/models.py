from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class AuditLog(models.Model):
    ACTION_CHOICES = [
        ('LOGIN', 'User Login'),
        ('LOGOUT', 'User Logout'),
        ('VIEW', 'Data View'),
        ('REQUEST', 'Data Request'),
        ('APPROVE', 'Request Approval'),
        ('DENY', 'Request Denial'),
        ('CONSENT', 'Consent Response'),
        ('OVERRIDE', 'Consent Override'),
        ('SHARE', 'Data Sharing'),
        ('HOD_NOTIFY', 'HOD Notification'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    patient = models.ForeignKey('patients.Patient', on_delete=models.SET_NULL, null=True, blank=True)
    request = models.ForeignKey('requests.DataRequest', on_delete=models.SET_NULL, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.timestamp} - {self.user} - {self.get_action_display()}"
    
    class Meta:
        ordering = ['-timestamp']