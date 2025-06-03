from django.urls import path
from . import views

urlpatterns = [
    path('new/', views.request_data, name='request_data'),
    path('hrio/', views.hrio_request_list, name='hrio_request_list'),
    path('hrio/<int:pk>/', views.handle_request, name='handle_request'),
    path('hod/notifications/', views.hod_notifications, name='hod_notifications'),
    path('hod/notifications/<int:pk>/', views.respond_notification, name='respond_notification'),
]