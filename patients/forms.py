from django import forms
from .models import Patient, PatientRecord

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = '__all__'
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }

class PatientRecordForm(forms.ModelForm):
    class Meta:
        model = PatientRecord
        fields = '__all__'
        exclude = ['created_by', 'data_hash']