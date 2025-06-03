from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages

class UserRoleMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Skip for static files and unauthorized page
        if request.path.startswith('/static/') or request.path == reverse('unauthorized'):
            return self.get_response(request)
            
        if request.user.is_authenticated:
            # Refresh user data from database
            from django.contrib.auth import get_user_model
            User = get_user_model()
            try:
                request.user = User.objects.get(pk=request.user.pk)
            except User.DoesNotExist:
                from django.contrib.auth import logout
                logout(request)
                messages.error(request, "Your account no longer exists")
                return redirect('login')

        response = self.get_response(request)
        return response