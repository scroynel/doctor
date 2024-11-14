from django.db.models.base import Model as Model
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, UpdateView, CreateView, FormView
from django.views.generic.edit import FormMixin
from django.shortcuts import get_object_or_404
from django.http import HttpResponseForbidden
from .models import Doctor, number_of_doctor
from .forms import DoctorAddFrom, CommentAddFrom
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from .decorators import only_for_doctors


class MainView(ListView):
    model = Doctor
    template_name = 'doctor/main.html'
    context_object_name = 'doctors'
    

    def get_queryset(self):
        return Doctor.objects.all()
    

class DoctorDetailView(FormMixin, DetailView):
    model=Doctor
    template_name = 'doctor/doctor_detail.html'
    slug_url_kwarg = 'doctor_slug'
    context_object_name = 'doctor'
    form_class = CommentAddFrom


    def get_object(self):
        return get_object_or_404(Doctor, slug=self.kwargs[self.slug_url_kwarg])
    

    def get_success_url(self):
        return reverse('doctor_detail', kwargs={'doctor_slug': self.kwargs[self.slug_url_kwarg]})
    

    def get_context_data(self, **kwargs):
        context = super(DoctorDetailView, self).get_context_data(**kwargs)
        context['form'] = self.get_form()
        return context
    

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        self.object = self.get_object()
        
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
   

    def form_valid(self, form):
        f = form.save(commit=False)
        f.doctor = self.get_object()
        f.from_user = self.request.user
        f.save()
        return super(DoctorDetailView, self).form_valid(form)
     

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
        return Doctor.objects.filter(specialty__slug=self.kwargs['specialty_slug'])
    