from django.db import IntegrityError
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from accounts.decorators import hrio_required, requester_required, hod_required
from accounts.models import CustomUser
from patients.models import Patient
from .models import DataRequest, Consent, DepartmentNotification
from .forms import DataRequestForm, ConsentForm, DepartmentNotificationForm
from audit.models import AuditLog

@login_required
@requester_required
def request_data(request):
    if request.method == 'POST':
        form = DataRequestForm(request.POST)
        if form.is_valid():
            # Get HRIO for the requester's facility
            hrio = CustomUser.objects.filter(
                role='HRIO',
                facility=request.user.facility
            ).first()
            
            if not hrio:
                messages.error(request, "No HRIO available for your facility. Please contact administration.")
                return redirect('dashboard')
            
            try:
                data_request = form.save(commit=False)
                data_request.requester = request.user
                data_request.hrio = hrio
                data_request.save()
                
                messages.success(request, "Your request has been submitted successfully!")
                return redirect('dashboard')
                
            except IntegrityError:
                messages.error(request, "An error occurred while processing your request. Please try again.")
                return redirect('request_data')
    else:
        form = DataRequestForm()
    
    return render(request, 'requests/request_form.html', {'form': form})

@login_required
@hrio_required
def hrio_request_list(request):
    pending_requests = DataRequest.objects.filter(
        hrio=request.user,
        status='PENDING',
        expires_at__gt=timezone.now()
    ).select_related('patient', 'requester')
    
    return render(request, 'requests/hrio_request_list.html', {
        'requests': pending_requests
    })

@login_required
@hrio_required
def handle_request(request, pk):
    data_request = get_object_or_404(DataRequest, pk=pk, hrio=request.user)
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'approve':
            # Check if consent already exists
            consent, created = Consent.objects.get_or_create(
                request=data_request,
                defaults={'response': 'PENDING'}
            )
            
            if data_request.patient.status in ['CHRONIC', 'CRITICAL']:
                justification = request.POST.get('justification', '').strip()
                if not justification:
                    messages.error(request, "Justification is required for chronic/critical patients")
                    return redirect('handle_request', pk=pk)
                
                consent.response = 'OVERRIDDEN'
                consent.override_justification = justification
                consent.save()
            else:
                if not created:  # Only send consent request if it's new
                    consent.response = 'PENDING'
                    consent.save()
                    messages.info(request, "Consent request sent to patient")
            
            # Get department from the patient's most recent record
            latest_record = data_request.patient.records.order_by('-created_at').first()
            department = latest_record.department if latest_record else 'Unknown'
            
            # Notify department head if exists
            hod = CustomUser.objects.filter(
                role='HOD',
                department=department,
                facility=request.user.facility
            ).first()
            
            if hod:
                DepartmentNotification.objects.get_or_create(
                    request=data_request,
                    hod=hod
                )
                messages.info(request, f"Notification sent to {hod.get_full_name()}")
            
            data_request.status = 'APPROVED'
            data_request.save()
            
            messages.success(request, "Request approved successfully")
            return redirect('hrio_request_list')
        
        elif action == 'deny':
            data_request.status = 'DENIED'
            data_request.save()
            messages.success(request, "Request denied")
            return redirect('hrio_request_list')
    
    return render(request, 'requests/handle_request.html', {
        'data_request': data_request
    })
@login_required
@hod_required
def hod_notifications(request):
    notifications = DepartmentNotification.objects.filter(
        hod=request.user,
        request__status='APPROVED'
    ).order_by('-request__created_at')
    
    return render(request, 'requests/hod_notifications.html', {'notifications': notifications})

@login_required
@hod_required
def respond_notification(request, pk):
    notification = get_object_or_404(DepartmentNotification, pk=pk, hod=request.user)
    
    if request.method == 'POST':
        form = DepartmentNotificationForm(request.POST, instance=notification)
        if form.is_valid():
            notification = form.save(commit=False)
            notification.responded_at = timezone.now()
            notification.save()
            
            AuditLog.objects.create(
                user=request.user,
                action='HOD_NOTIFY',
                description=f"HOD responded to notification for request #{notification.request.id}",
                patient=notification.request.patient,
                request=notification.request
            )
            
            messages.success(request, "Your response has been recorded")
            return redirect('hod_notifications')
    else:
        form = DepartmentNotificationForm(instance=notification)
    
    return render(request, 'requests/respond_notification.html', {
        'form': form,
        'notification': notification
    })