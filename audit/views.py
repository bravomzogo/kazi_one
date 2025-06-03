from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from .models import AuditLog

def audit_logs(request):
    # Get all logs ordered by timestamp (newest first)
    logs_list = AuditLog.objects.select_related('user', 'patient').order_by('-timestamp')
    
    # Pagination - 25 items per page
    paginator = Paginator(logs_list, 25)
    page = request.GET.get('page')
    
    try:
        logs = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page
        logs = paginator.page(1)
    except EmptyPage:
        # If page is out of range, deliver last page
        logs = paginator.page(paginator.num_pages)
    
    context = {
        'logs': logs,
        'debug': False  # Set to True temporarily for debugging
    }
    return render(request, 'audit/logs.html', context)