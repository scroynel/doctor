from django.db.models.base import Model as Model
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, PasswordChangeView
from .forms import LoginForm, RegisterForm, UserPasswordChangeForm

from django.views.generic import CreateView, DetailView
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.shortcuts import get_object_or_404


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
        return get_object_or_404(get_user_model(), pk=self.kwargs[self.pk_url_kwarg])
    

class UserPasswordChangeView(PasswordChangeView):
    template_name = 'users/password_change_form.html'
    form_class = UserPasswordChangeForm
    success_url = reverse_lazy('users:password_change_done')
