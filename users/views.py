from django.db.models.base import Model as Model
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, PasswordChangeView
from .forms import LoginForm, RegisterForm, UserPasswordChangeForm

from django.views.generic import CreateView, DetailView
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.shortcuts import get_object_or_404

from doctor.models import Appointment
import datetime

from .models import User


class LoginUser(LoginView):
    template_name = 'users/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('main')
    title = 'Log In'


class RegisterUser(CreateView):
    template_name = 'users/register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('users:login')


    def form_valid(self, form: RegisterForm):
        f = form.save(commit=False)
        if form.cleaned_data['as_doctor'] == 'True':
            group = Group.objects.get(name='Doctors')
        else:
            group = Group.objects.get(name='Patients')
        f.save()
        f.groups.add(group)
    
        return super().form_valid(form)


class ProfileUser(DetailView):
    template_name = 'users/profile.html'
    context_object_name = 'profile'


    def get_object(self):
        self.appoitments_list(self.request.user)
        return User.objects.get(pk=self.kwargs[self.pk_url_kwarg])
    
    
    # Appointments list only with appointment date < current time, if current time > appointment date --> delete an appointment
    @staticmethod
    def appoitments_list(user):
        user_appointments = Appointment.objects.filter(patient=user)
        for appointment in user_appointments:
            if appointment.appointment_date.date() < datetime.datetime.now().date():
                if appointment.appointment_date.time() < datetime.datetime.now().time():
                    appointment.delete()
        return user_appointments
    

class UserPasswordChangeView(PasswordChangeView):
    template_name = 'users/password_change_form.html'
    form_class = UserPasswordChangeForm
    success_url = reverse_lazy('users:password_change_done')
