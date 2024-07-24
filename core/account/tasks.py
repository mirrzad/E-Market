from django.utils import timezone
from .models import Otp
from celery import shared_task


@shared_task
def remove_expired_otp_codes_task():
    expired_time = timezone.now() - timezone.timedelta(minutes=1)
    Otp.objects.filter(created_time__lt=expired_time).delete()
