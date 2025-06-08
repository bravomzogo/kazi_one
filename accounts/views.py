from django.utils import timezone
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from requests.models import DataRequest
from .forms import CustomUserCreationForm, LoginForm
from .decorators import hrio_required, requester_required, hod_required
from audit.models import AuditLog

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            AuditLog.objects.create(
                user=user,
                action='REGISTER',
                ip_address=request.META.get('REMOTE_ADDR')
            )
            messages.success(request, "Registration successful!")
            return redirect('dashboard')
        else:
            messages.error(request, "Registration failed. Please correct the errors.")
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                AuditLog.objects.create(
                    user=user,
                    action='LOGIN',
                    ip_address=request.META.get('REMOTE_ADDR')
                )
                messages.success(request, "Logged in successfully!")
                return redirect('dashboard')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid form submission.")
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})

def user_logout(request):
    if request.user.is_authenticated:
        AuditLog.objects.create(
            user=request.user,
            action='LOGOUT',
            ip_address=request.META.get('REMOTE_ADDR')
        )
    logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect('login')

@login_required
def dashboard(request):
    user = request.user
    context = {'user': user}
    
    if user.role == 'HRIO':
        pending_requests = DataRequest.objects.filter(
            hrio=user,
            status='PENDING',
            expires_at__gt=timezone.now()
        ).select_related('patient', 'requester')
        context['pending_requests'] = pending_requests
        return render(request, 'accounts/hrio_dashboard.html', context)
    elif user.role in ['DOCTOR', 'NURSE', 'PHARMACIST', 'ICT']:
        return render(request, 'accounts/requester_dashboard.html', context)
    elif user.role == 'HOD':
        return render(request, 'accounts/hod_dashboard.html', context)
    else:
        return render(request, 'accounts/admin_dashboard.html', context)

def unauthorized(request):
    return render(request, 'accounts/unauthorized.html', status=403)