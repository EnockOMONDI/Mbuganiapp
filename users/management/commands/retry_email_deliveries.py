from django.core.management.base import BaseCommand
from django.utils import timezone
from users.models import EmailDelivery
from users.tasks import deliver_email

class Command(BaseCommand):
    help = 'Retry up to 50 pending email deliveries, with at most three attempts per message.'

    def handle(self, *args, **options):
        ids = list(EmailDelivery.objects.filter(sent_at__isnull=True, attempts__lt=3,
                    next_attempt_at__lte=timezone.now()).order_by('created_at').values_list('pk', flat=True)[:50])
        sent = sum(deliver_email(pk) for pk in ids)
        self.stdout.write(f'{sent}/{len(ids)} pending emails delivered.')
