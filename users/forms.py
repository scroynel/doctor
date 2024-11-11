from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth import get_user_model


class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Login', widget=forms.TextInput())
    password = forms.CharField(label='Password', widget=forms.PasswordInput())


    class Meta:
        model = get_user_model()
        fields = ['username', 'password']


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for f in self.fields:
            self.fields[f].widget.attrs.update({'class': 'w-full rounded', 'placeholder': f'{self.fields[f].label}'})


class RegisterForm(UserCreationForm):
    username = forms.CharField(label='Login')
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput())
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput())
    as_doctor = forms.CharField(label='As Doctor', widget=forms.CheckboxInput(), required=False)
    usable_password = None
   

    class Meta:
        model = get_user_model()
        fields = ['photo', 'username', 'email', 'first_name', 'last_name', 'password1', 'password2', 'as_doctor']
        excludes = ['usable_password']
        labels = {
            'email': 'Email',
            'first_name': 'Name',
            'last_name': 'Surname'
        }


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for f in self.fields:
            self.fields[f].widget.attrs.update({'class': 'w-full rounded', 'placeholder': f'{self.fields[f].label}'})
        self.fields['as_doctor'].widget.attrs.update({'class': 'rounded'})


    def clean_email(self):
        email = self.cleaned_data['email']
        if get_user_model().objects.filter(email=email):
            raise forms.ValidationError('The Email already exists')
        return email
    

class UserPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label='Old password', widget=forms.PasswordInput())
    new_password1 = forms.CharField(label='New password', widget=forms.PasswordInput())
    new_password2 = forms.CharField(label='Repeat new password', widget=forms.PasswordInput())


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for f in self.fields:
             self.fields[f].widget.attrs.update({'class': 'w-full rounded', 'placeholder': f'{self.fields[f].label}'})


class UserPasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for f in self.fields:
            self.fields[f].widget.attrs.update({'class': 'w-full rounded', 'placeholder': f'{self.fields[f].label}'})


class UserSetPasswordFrom(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for f in self.fields:
            self.fields[f].widget.attrs.update({'class': 'w-full rounded', 'placeholder': f'{self.fields[f].label}'})