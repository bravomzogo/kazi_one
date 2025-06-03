from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.utils import timezone
from .models import Patient, PatientRecord
from .forms import PatientForm, PatientRecordForm
from accounts.decorators import hrio_required

@login_required
@hrio_required
def patient_list(request):
    patients = Patient.objects.all().order_by('-created_at')
    return render(request, 'patients/patient_list.html', {'patients': patients})

@login_required
@hrio_required
def patient_detail(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    records = patient.records.all().order_by('-created_at')
    return render(request, 'patients/patient_detail.html', {
        'patient': patient,
        'records': records
    })

@login_required
@hrio_required
def patient_create(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            patient = form.save(commit=False)
            patient.created_by = request.user
            patient.save()
            return redirect('patient_detail', pk=patient.pk)
    else:
        form = PatientForm()
    
    return render(request, 'patients/patient_form.html', {
        'form': form,
        'title': 'Add New Patient'
    })

@login_required
@hrio_required
def record_create(request, patient_pk):
    patient = get_object_or_404(Patient, pk=patient_pk)
    if request.method == 'POST':
        form = PatientRecordForm(request.POST)
        if form.is_valid():
            record = form.save(commit=False)
            record.patient = patient
            record.created_by = request.user
            record.save()
            return redirect('patient_detail', pk=patient.pk)
    else:
        form = PatientRecordForm()
    
    return render(request, 'patients/record_form.html', {
        'form': form,
        'patient': patient,
        'title': 'Add Medical Record'
    })

@login_required
def patient_search(request):
    query = request.GET.get('q', '').strip()
    
    if not query:
        return redirect('patient_list')
    
    patients = Patient.objects.filter(
        Q(patient_number__icontains=query) |
        Q(first_name__icontains=query) |
        Q(last_name__icontains=query)
    ).distinct().order_by('-created_at')
    
    records = PatientRecord.objects.filter(
        Q(diagnosis__icontains=query) |
        Q(treatment__icontains=query) |
        Q(notes__icontains=query)
    ).select_related('patient').order_by('-created_at')
    
    return render(request, 'patients/search_results.html', {
        'patients': patients,
        'records': records,
        'query': query
    })