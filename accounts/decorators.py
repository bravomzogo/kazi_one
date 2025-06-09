from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from django.shortcuts import redirect

def hrio_required(view_func):
    def check_hrio(user):
        if not user.is_authenticated:
            messages.error(user, "You must be logged in to access this page.")
            return False
        if user.role != 'HRIO':
            messages.error(user, "You are not authorized to access this page.")
            return False
        return True
    return user_passes_test(check_hrio, login_url='unauthorized')(view_func)

def requester_required(view_func):
    def check_requester(user):
        if not user.is_authenticated:
            messages.error(user, "You must be logged in to access this page.")
            return False
        if user.role not in ['DOCTOR', 'NURSE', 'PHARMACIST', 'ICT', 'RESEARCHER']:
            messages.error(user, "You are not authorized to access this page.")
            return False
        return True
    return user_passes_test(check_requester, login_url='unauthorized')(view_func)

def hod_required(view_func):
    def check_hod(user):
        if not user.is_authenticated:
            messages.error(user, "You must be logged in to access this page.")
            return False
        if user.role != 'HOD':
            messages.error(user, "You are not authorized to access this page.")
            return False
        return True
    return user_passes_test(check_hod, login_url='unauthorized')(view_func)

def admin_required(view_func):
    def check_admin(user):
        if not user.is_authenticated:
            messages.error(user, "You must be logged in to access this page.")
            return False
        if user.role != 'ADMIN':
            messages.error(user, "You are not authorized to perform this action.")
            return False
        return True
    return user_passes_test(check_admin, login_url='unauthorized')(view_func)

def admin_or_hrio_required(view_func):
    def check_admin_or_hrio(user):
        if not user.is_authenticated:
            messages.error(user, "You must be logged in to access this page.")
            return False
        if user.role not in ['ADMIN', 'HRIO']:
            messages.error(user, "You are not authorized to perform this action.")
            return False
        return True
    return user_passes_test(check_admin_or_hrio, login_url='unauthorized')(view_func)