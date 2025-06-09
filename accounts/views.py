from django.utils import timezone
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import CustomUser
from requests.models import DataRequest
from .forms import CustomUserCreationForm, LoginForm, ResearcherForm
from .decorators import hrio_required, requester_required, hod_required
from audit.models import AuditLog
from functools import wraps
from django.http import FileResponse
from django.core.exceptions import PermissionDenied

# Custom decorator for admin role
def admin_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.role != 'ADMIN':
            messages.error(request, "You are not authorized to perform this action.")
            return redirect('unauthorized')
        return view_func(request, *args, **kwargs)
    return wrapper

# Custom decorator for admin or HRIO role
def admin_or_hrio_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.role not in ['ADMIN', 'HRIO']:
            messages.error(request, "You are not authorized to perform this action.")
            return redirect('unauthorized')
        return view_func(request, *args, **kwargs)
    return wrapper

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
    elif user.role in ['DOCTOR', 'NURSE', 'PHARMACIST', 'ICT', 'RESEARCHER']:
        return render(request, 'accounts/requester_dashboard.html', context)
    elif user.role == 'HOD':
        return render(request, 'accounts/hod_dashboard.html', context)
    else:
        return render(request, 'accounts/admin_dashboard.html', context)

def unauthorized(request):
    return render(request, 'accounts/unauthorized.html', status=403)

@login_required
@admin_or_hrio_required
def add_researcher(request):
    if request.method == 'POST':
        form = ResearcherForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            AuditLog.objects.create(
                user=request.user,
                action='ADD_RESEARCHER',
                ip_address=request.META.get('REMOTE_ADDR'),
                # description=f"Added researcher {user.username}"
            )
            messages.success(request, "Researcher added successfully!")
            return redirect('dashboard')
        else:
            messages.error(request, "Failed to add researcher. Please correct the errors.")
    else:
        form = ResearcherForm()
    return render(request, 'accounts/add_researcher.html', {'form': form})






@login_required
def researcher_info(request):
    # Only HRIO and ADMIN can access this view
    if request.user.role not in ['HRIO', 'ADMIN']:
        raise PermissionDenied("You don't have permission to view this page")
    
    researchers = CustomUser.objects.filter(role='RESEARCHER').select_related('researcher_profile')
    context = {
        'researchers': researchers,
    }
    return render(request, 'accounts/researcher_info.html', context)

@login_required
def download_hr_document(request, researcher_id):
    # Only HRIO and ADMIN can download
    if request.user.role not in ['HRIO', 'ADMIN']:
        raise PermissionDenied("You don't have permission to download this file")
    
    researcher = CustomUser.objects.get(id=researcher_id)
    profile = researcher.researcher_profile
    return FileResponse(profile.hr_document.open(), as_attachment=True)