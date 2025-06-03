from django.utils import timezone 
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

from requests.models import DataRequest
from .forms import CustomUserCreationForm, LoginForm
from .decorators import hrio_required, requester_required, hod_required

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
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
                return redirect('dashboard')
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard(request):
    user = request.user
    context = {'user': user}
    
    if user.role == 'HRIO':
        # Get pending requests for HRIO dashboard
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
    else:  # Admin or other roles
        return render(request, 'accounts/admin_dashboard.html', context)
    


def unauthorized(request):
    return render(request, 'accounts/unauthorized.html', status=403)