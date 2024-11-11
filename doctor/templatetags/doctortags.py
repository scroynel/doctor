from django import template
from doctor.models import Specialty
from django.db.models import Count
from django.contrib.auth import get_user_model

register = template.Library()

@register.inclusion_tag('doctor/list_specialty.html')
def list_specialty():
    specialties = Specialty.objects.annotate(total=Count('doctors')).filter(total__gt=0)
    return {'specialties': specialties}