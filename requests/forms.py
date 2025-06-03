from django import forms
from .models import Consent, DataRequest, DepartmentNotification

class DataRequestForm(forms.ModelForm):
    class Meta:
        model = DataRequest
        fields = ['patient', 'purpose']
        
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if self.user and self.user.role == 'HRIO':
            self.fields['hrio'].initial = self.user

class ConsentForm(forms.ModelForm):
    class Meta:
        model = Consent
        fields = ['response', 'override_justification']
        widgets = {
            'override_justification': forms.Textarea(attrs={'rows': 3}),
        }

class DepartmentNotificationForm(forms.ModelForm):
    class Meta:
        model = DepartmentNotification
        fields = ['response']