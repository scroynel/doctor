from django.urls import path

from . import views

urlpatterns = [
    path('', views.MainView.as_view(), name='main'),
    path('doctor/<slug:doctor_slug>/', views.DoctorDetailView.as_view(), name='doctor_detail'),
    path('add-doctor/', views.DoctorAddView.as_view(), name='doctor_add'),
    path('edit/<slug:edit_slug>/', views.DoctorUpdateView.as_view(), name='doctor_edit'),
    path('specialty/<slug:specialty_slug>', views.DoctorsBySpecialty.as_view(), name='doctors_by_specialty'),
]
