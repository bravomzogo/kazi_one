from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser
from django.core.exceptions import ValidationError
import os

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'facility', 'role', 'department')

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'facility', 'role', 'department')

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class ResearcherForm(CustomUserCreationForm):
    company = forms.CharField(max_length=100, required=True, help_text="Company or organization the researcher works for")
    data_sought = forms.CharField(widget=forms.Textarea(attrs={'rows': 4}), required=True, help_text="Description of the data the researcher is seeking")
    hr_document = forms.FileField(required=True, help_text="Upload HR approval document (PDF only)")

    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email', 'phone_number',  'company', 'data_sought', 'hr_document', 'password1', 'password2')

    def clean_hr_document(self):
        hr_document = self.cleaned_data.get('hr_document')
        if hr_document:
            # Check file extension
            ext = os.path.splitext(hr_document.name)[1].lower()
            if ext != '.pdf':
                raise ValidationError("Only PDF files are allowed.")
            # Optional: Check file size (e.g., limit to 5MB)
            if hr_document.size > 5 * 1024 * 1024:
                raise ValidationError("File size must be under 5MB.")
        return hr_document

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'RESEARCHER'  # Enforce RESEARCHER role
        if commit:
            user.save()
            # Save additional fields (company, data_sought, hr_document) to a related model if needed
            # For simplicity, store hr_document in media storage
            self.instance.hr_document = self.cleaned_data['hr_document']
        return user