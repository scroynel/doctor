from django.db.models.base import Model as Model
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from django.views.generic.edit import FormMixin
from django.shortcuts import get_object_or_404, redirect, render
from .models import Doctor, number_of_doctor, Notification, Appointment
from .forms import DoctorAddFrom, CommentAddFrom, DateForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from .decorators import only_for_doctors
import json
import pandas as pd 

from django.core.exceptions import ObjectDoesNotExist

from .red_cch import get_data

class MainView(ListView):
    model = Doctor
    template_name = 'doctor/main.html'
    context_object_name = 'doctors'
    

    def get_queryset(self):
        doctors = Doctor.objects.prefetch_related('specialty').filter()
        return get_data(doctors)
    

class DoctorDetailView(DetailView, FormMixin):
    model = Doctor
    template_name = 'doctor/doctor_detail.html'
    slug_url_kwarg = 'doctor_slug'
    context_object_name = 'doctor'
    form_class = CommentAddFrom
    second_form_class = DateForm

    def get_object(self):
        return Doctor.objects.prefetch_related('comments__from_user').get(slug=self.kwargs[self.slug_url_kwarg])
    

    def get_success_url(self):
        return reverse('doctor_detail', kwargs={'doctor_slug': self.kwargs[self.slug_url_kwarg]})
    

    def get_context_data(self, **kwargs):
        context = super(DoctorDetailView, self).get_context_data(**kwargs)
        if 'form' not in context:
            context['form'] = self.form_class()
        if 'form2' not in context:
            context['form2'] = self.second_form_class()
        context['time_list'] = self.get_object().work_hours.all
        for i in self.get_object().work_hours.all():
            context[f'weekday{i.weekday}'] = json.dumps(self.list_of_working_hours(i.from_time.strftime('%H:%M'), i.to_time.strftime('%H:%M')))
        return context
    

    #create list of workng hours for a doctor (This is need for datetimepicker appointments)
    @staticmethod
    def list_of_working_hours(from_time, to_time):
        result = pd.date_range(from_time, to_time, freq='60min').strftime('%H:%M')
        # for time in range(from_time.hour, to_time.hour + 1):
        #     result.append(datetime.time(time, from_time.minute).strftime('%H:%M'))
        return list(result)


    def form_invalid(self, **kwargs):
        return self.render_to_response(self.get_context_data(**kwargs))
    

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        if 'form' in request.POST:
            form_class = self.form_class(request.POST)
            if form_class.is_valid():
                f = form_class.save(commit=False)
                f.doctor = self.get_object()
                f.from_user = self.request.user
                f.save()
                Notification.objects.create(user=self.get_object().owner, message=f'{self.request.user} left a comment for your doctor.') 
                return render(request, 'doctor/partials/comment_list.html', {'doctor': self.object})
            else:
                return self.form_invalid(form_class)
        else:
            form_class = self.second_form_class(request.POST)
            if form_class.is_valid():
                f = form_class.save(commit=False)
                f.doctor = self.get_object()
                f.patient = request.user
                f.save()
                return redirect('users:profile', request.user.id)
            else:
                return self.form_invalid(form_class)

@method_decorator(only_for_doctors('Doctors'), 'dispatch')
class DoctorAddView(LoginRequiredMixin, CreateView):
    model = Doctor
    excludes = ['slug']
    form_class = DoctorAddFrom
    template_name = 'doctor/doctor_add.html'
    success_url = reverse_lazy('main')


    def form_valid(self, form):
        f = form.save(commit=False)
        f.slug = f'{f.name.lower()}-{f.surname.lower()}-{f.number}'
        f.number = number_of_doctor()
        f.owner = self.request.user
        f.save()
        return super().form_valid(form)
        
    
@method_decorator(only_for_doctors('Doctors'), 'dispatch')
class DoctorUpdateView(LoginRequiredMixin, UpdateView):
    model = Doctor
    template_name = 'doctor/doctor_edit.html'
    form_class = DoctorAddFrom
    slug_url_kwarg = 'edit_slug'
    success_url = reverse_lazy('main')


    def form_valid(self, form):
        f = form.save(commit=False)
        f.slug = f'{f.name.lower()}-{f.surname.lower()}-{f.number}'
        f.save()
        return super().form_valid(form)


class DoctorsBySpecialty(ListView):
    model = Doctor
    template_name = 'doctor/main.html'
    context_object_name = 'doctors'


    def get_queryset(self):
        doctors =  Doctor.objects.prefetch_related('specialty').filter(specialty__slug=self.kwargs['specialty_slug'])
        return doctors
    
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def appointment_delete(request, pk):
    Appointment.objects.filter(pk=pk).delete()
    return render(request, 'doctor/partials/appointment_list.html', {'profile': request.user})