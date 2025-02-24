from django.db import models
from django.contrib.auth import get_user_model
import random

from django.urls import reverse


WEEKDAYS = (
    (1, "Monday"),
    (2, "Tuesday"),
    (3, "Wednesday"),
    (4, "Thursday"),
    (5, "Friday"),
    (6, "Saturday"),
    (7, "Sunday"),
)


# Number of doctor
def number_of_doctor():
    return random.randint(100000, 999999)


class Doctor(models.Model):
    image = models.ImageField(upload_to='doctor_images', blank=True)
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    number = models.PositiveIntegerField(unique=True, default=number_of_doctor)
    slug = models.SlugField(max_length=255, db_index=True, blank=True)
    age = models.PositiveIntegerField()
    description = models.TextField()
    experience = models.PositiveIntegerField()
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    specialty = models.ForeignKey('Specialty', on_delete=models.CASCADE, related_name='doctors')
    owner = models.OneToOneField(get_user_model(), null=True, blank=True, on_delete=models.CASCADE, related_name='doctor', limit_choices_to={'groups__name': 'Doctors'})


    def __str__(self):
        return self.name + ' ' + self.surname


    def get_absolute_url(self):
        return reverse('doctor_detail', kwargs={'doctor_slug': self.slug,})


    class Meta:
        verbose_name = 'Doctor'
        verbose_name_plural = 'Doctors'


class Specialty(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)
    

    def __str__(self):
        return self.name
    

    def get_absolute_url(self):
        return reverse('doctors_by_specialty', kwargs={'specialty_slug': self.slug})
    

    class Meta:
        verbose_name = 'Specialty'
        verbose_name_plural = 'specialties'


class DoctorFeedback(models.Model):
    description = models.TextField()
    time_create = models.DateTimeField(auto_now_add=True)
    star = models.FloatField(default=0)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='comments')
    from_user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='comments_to')


    def __str__(self):
        return f'{self.doctor.name} -- {self.star}'
    
    
    class Meta:
        ordering = ['-time_create']


class Notification(models.Model):
    is_read = models.BooleanField(default=False)
    message = models.TextField()
    time_create = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='notification')


    def get_absolute_url(self):
        return reverse('doctor_detail', kwargs={'doctor_slug': self.user.doctor.slug})
    

class Appointment(models.Model):
    appointment_date = models.DateTimeField()
    create_date = models.DateTimeField(auto_now_add=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='doctor_appointments')
    patient = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='user_appointments')

    
    def __str__(self):
        return f'Doctor {self.doctor.name} - {self.appointment_date.strftime('%Y/%m/%d - %H:%M')} - {self.patient.username}'
    
    
    class Meta:
        ordering = ['appointment_date']


class WorkingHours(models.Model):
    doctor = models.ForeignKey('Doctor', on_delete=models.CASCADE, related_name='work_hours')
    weekday = models.IntegerField(choices=WEEKDAYS, unique=True)
    from_time = models.TimeField()
    to_time = models.TimeField()


    def __str__(self):
        return f'{self.doctor} -- {self.weekday} day of the week -- from {self.from_time} to {self.to_time}'

    
    class Meta:
        verbose_name = 'Working hour'
        verbose_name_plural = 'Working hours'