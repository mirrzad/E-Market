from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import UserManager
from django.utils import timezone


class User(AbstractBaseUser, PermissionsMixin):
    phone_number = models.CharField(max_length=11, unique=True)
    email = models.EmailField(max_length=50, unique=True)
    full_name = models.CharField(max_length=50, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.email

    @property
    def is_staff(self):
        return self.is_superuser


class Otp(models.Model):
    phone_number = models.CharField(max_length=11, unique=True)
    code = models.IntegerField()
    created_time = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_time']

    def __str__(self):
        return f'{self.phone_number} - {self.code} - {self.created_time}'

    @property
    def is_expired(self):
        return timezone.now() > (self.created_time + timezone.timedelta(minutes=1))
