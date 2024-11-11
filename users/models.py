from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    photo = models.ImageField(verbose_name='Image', upload_to='user_images', null=True, blank=True, default='user_default.png')