from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=20, blank=True, verbose_name='Номер телефона')
    city = models.CharField(max_length=100, blank=True, verbose_name='Город')
    address = models.TextField(blank=True, verbose_name='Адрес')

    def __str__(self):
        return f'Профиль {self.user.username}'
