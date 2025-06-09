from django.urls import path
from . import views

urlpatterns = [
    path('register', views.register, name='register'),
    path('', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('unauthorized/', views.unauthorized, name='unauthorized'),
    path('add-researcher/', views.add_researcher, name='add_researcher'),
    path('researcher-info/', views.researcher_info, name='researcher_info'),
    path('download-hr-document/<int:researcher_id>/', views.download_hr_document, name='download_hr_document'),
]