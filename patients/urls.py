from django.urls import path
from . import views

urlpatterns = [
    path('', views.patient_list, name='patient_list'),
    path('new/', views.patient_create, name='patient_create'),
    path('<int:pk>/', views.patient_detail, name='patient_detail'),
    path('<int:patient_pk>/records/new/', views.record_create, name='record_create'),
    path('search/', views.patient_search, name='patient_search'),
]