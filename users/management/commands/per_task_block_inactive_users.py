from django.core.management import BaseCommand
from users.models import User
from django.contrib.auth.models import Group
from django_celery_beat.models import PeriodicTask, IntervalSchedule
from datetime import datetime, timedelta


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        schedule, created = IntervalSchedule.objects.get_or_create(
            every=1,
            period=IntervalSchedule.DAYS,
        )

        PeriodicTask.objects.create(
            interval=schedule,
            name='Block users inactive for 30+ days',
            task='users.services.last_login_blocker',
            start_time=datetime.now(),
            description='Block users inactive for 30+ days'
        )

