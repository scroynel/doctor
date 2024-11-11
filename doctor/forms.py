from django import forms
from django.utils.safestring import mark_safe
from django.core.exceptions import ValidationError
from .models import Doctor, Specialty, DoctorFeedback


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
        for f in self.fields:
            self.fields[f].widget.attrs.update({'class': 'w-full rounded-xl', 'placeholder': f'{f.capitalize()}', 'rows': '3'})