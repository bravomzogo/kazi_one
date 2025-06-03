from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect

def hrio_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if request.user.role == 'HRIO':
            return view_func(request, *args, **kwargs)
        return redirect('unauthorized')
    return _wrapped_view

def requester_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if request.user.role in ['DOCTOR', 'NURSE', 'PHARMACIST', 'ICT']:
            return view_func(request, *args, **kwargs)
        return redirect('unauthorized')
    return _wrapped_view

def hod_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if request.user.role == 'HOD':
            return view_func(request, *args, **kwargs)
        return redirect('unauthorized')
    return _wrapped_view