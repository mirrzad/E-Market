from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from .managers import UserManager
from django.utils import timezone


class User(AbstractBaseUser):
    phone_number = models.CharField(max_length=11, unique=True)
    email = models.EmailField(max_length=50, unique=True)
    full_name = models.CharField(max_length=50, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin


class Otp(models.Model):
    phone_number = models.CharField(max_length=11)
    code = models.IntegerField()
    created_time = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_time']

    def __str__(self):
        return f'{self.phone_number} - {self.code} - {self.created_time}'

    @property
    def is_expired(self):
        return timezone.now() > (self.created_time + timezone.timedelta(minutes=1))




