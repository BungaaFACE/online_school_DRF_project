from django.core.management import BaseCommand
from users.models import User
from django.contrib.auth.models import Group


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        user = User.objects.create(
            email='user1@gmail.com',
            first_name='user',
            last_name='user',
            is_active=True,
            is_staff=False,
            is_superuser=False,
        )

        user.set_password('user')
        user.save()

        user = User.objects.create(
            email='user2@gmail.com',
            first_name='user',
            last_name='user',
            is_active=True,
            is_staff=False,
            is_superuser=False,
        )

        user.set_password('user')
        user.save()

        user = User.objects.create(
            email='user3@gmail.com',
            first_name='user',
            last_name='user',
            is_active=True,
            is_staff=False,
            is_superuser=False,
        )

        user.set_password('user')
        user.save()

        user = User.objects.create(
            email='user4@gmail.com',
            first_name='user',
            last_name='user',
            is_active=True,
            is_staff=False,
            is_superuser=False,
        )

        user.set_password('user')
        user.save()

        user = User.objects.create(
            email='user5@gmail.com',
            first_name='user',
            last_name='user',
            is_active=True,
            is_staff=False,
            is_superuser=False,
        )

        user.set_password('user')
        user.save()

