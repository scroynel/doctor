from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Doctor, Specialty, DoctorFeedback, Notification, Appointment


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    fields = ['image', 'number', 'name', 'surname', 'slug', 'age', 'experience', 'specialty', 'description', 'owner']
    list_display = ['id', 'number', 'name', 'surname', 'age', 'experience', 'specialty', 'doctor_photo']
    list_display_links = ['number', 'name', 'surname']
    list_filter = ['age', 'experience', 'specialty']
    prepopulated_fields = {'slug': ('name', 'surname', 'number')}


    def doctor_photo(self, doctor: Doctor):
        if doctor.image:
            return mark_safe(f'<img src="{doctor.image.url}" width=50>')
        return 'No photo'
    

@admin.register(Specialty)
class SpecialtyAdmin(admin.ModelAdmin):
    model = Specialty
    list_display = ['id', 'name']
    list_display_links = ['id', 'name']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(DoctorFeedback)
class DoctorFeedbackAdmin(admin.ModelAdmin):
    list_display = ['id', 'doctor', 'from_user', 'description', 'star', 'time_create']


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['id', 'message', 'user', 'time_create', 'is_read']


admin.site.register(Appointment)