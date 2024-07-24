from django.core.management.base import BaseCommand
from django.utils import timezone
from account.models import Otp


class Command(BaseCommand):
    help = 'remove all expired otp codes in database.'

    def handle(self, *args, **options):
        expired_time = timezone.now() - timezone.timedelta(minutes=1)
        Otp.objects.filter(created_time__lt=expired_time).delete()
        self.stdout.write('All expired otp codes removed successfully.')
