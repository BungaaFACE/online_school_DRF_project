from django.core.management import BaseCommand
from online_school.models import Course, Lesson, Payment
from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **options) -> str | None:

        try:
            Payment.objects.all().delete()
        except:
            pass

        payment_list = [
            {'user': User.objects.get(email='user1@gmail.com'),
             'purchased_item': Course.objects.get(name='course 1'),
             'summ': 1000,
             'payment_type': 'card',
             },
            {'user': User.objects.get(email='user1@gmail.com'),
             'purchased_item': Course.objects.get(name='course 2'),
             'summ': 1000,
             'payment_type': 'card',
             },
            {'user': User.objects.get(email='user2@gmail.com'),
             'purchased_item': Course.objects.get(name='course 3'),
             'summ': 1000,
             'payment_type': 'card',
             },
            {'user': User.objects.get(email='user3@gmail.com'),
             'purchased_item': Lesson.objects.get(name='lesson 1', 
                                                  course=Course.objects.get(name='course 5')),
             'summ': 200,
             'payment_type': 'cash',
             },
            {'user': User.objects.get(email='user3@gmail.com'),
             'purchased_item': Lesson.objects.get(name='lesson 2', 
                                                  course=Course.objects.get(name='course 5')),
             'summ': 200,
             'payment_type': 'cash',
             },
        ]
        
        payment_instances = []
        for payment in payment_list:
            payment_instances.append(Payment(**payment))

        Payment.objects.bulk_create(payment_instances)