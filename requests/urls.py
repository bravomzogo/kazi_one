from django.urls import path
from . import views

urlpatterns = [
    path('request/', views.request_data, name='request_data'),
    path('hrio-requests/', views.hrio_request_list, name='hrio_request_list'),
    path('handle/<int:pk>/', views.handle_request, name='handle_request'),
    path('hod-notifications/', views.hod_notifications, name='hod_notifications'),
    path('respond/<int:pk>/', views.respond_notification, name='respond_notification'),
    path('view-approved/<int:pk>/', views.view_approved_data, name='view_approved_data'),
]