from django import forms
from django.core.exceptions import ValidationError
from .models import Doctor, Specialty, DoctorFeedback, Appointment
from project.settings import DATETIME_INPUT_FORMATS


class DoctorAddFrom(forms.ModelForm):
    image = forms.ImageField(widget=forms.FileInput)
    specialty = forms.ModelChoiceField(queryset=Specialty.objects.all(), empty_label='Specialty not selected')
    

    class Meta:
        model = Doctor
        exclude = ['slug', 'number', 'owner']


    def __init__(self, *args, **kwargs):
        super(DoctorAddFrom, self).__init__(*args, **kwargs)
        for f in self.fields:
            self.fields[f].widget.attrs.update({'class': 'w-full rounded', 'placeholder': f'{f.capitalize()}'})


    def clean_description(self):
        description = self.cleaned_data['description']
        if len(description) < 50:
            raise ValidationError('Description must contain more than 50 characters.')
        return description
    
    
class CommentAddFrom(forms.ModelForm):

    
    class Meta:
        model = DoctorFeedback
        fields = ['description', 'star']


    def __init__(self, *args, **kwargs):
        super(CommentAddFrom, self).__init__(*args, **kwargs)
        self.fields['description'].widget.attrs.update({'class': 'w-full rounded-xl', 'placeholder': 'Description...', 'rows': '3'})


class DateForm(forms.ModelForm):
    appointment_date = forms.DateTimeField(input_formats=DATETIME_INPUT_FORMATS, widget=forms.DateTimeInput(format=DATETIME_INPUT_FORMATS))


    class Meta:
        model = Appointment
        fields = ['appointment_date']

    def __init__(self, *args, **kwargs):
        super(DateForm, self).__init__(*args, **kwargs)
        self.fields['appointment_date'].widget.attrs.update({'placeholder': 'Select date...'})