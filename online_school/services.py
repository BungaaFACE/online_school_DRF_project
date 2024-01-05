from django.conf import settings
from online_school.models import CourseSubscribe, Payment, StripeSession
from django.core.mail import send_mail
from celery import shared_task
import stripe

class SendCourseUpdate:
    def __init__(self, course, message) -> None:
        
        self.mail_subject = f'Обновление курса {course.name}'
        self.message = message
        
        course_subscribes = CourseSubscribe.objects.filter(course=course)
        self.subscriber_mail_list = [sub.user.email for sub in course_subscribes]

    @shared_task
    def send_email(self):
        send_mail(
            self.mail_subject,
            self.message,
            settings.EMAIL_HOST_USER,
            self.subscriber_mail_list,
            fail_silently=False
        )


def update_stripe_sessions_status(user):
    """
    Функция обновляет статусы сессий stripe пользователя
    и, при необходимости, выставляет статусы оплачен или просрочен
    """
    not_paid_sessions = StripeSession.objects.filter(status='ожидание оплаты', user=user)
    for session in not_paid_sessions:
        stripe_session = stripe.checkout.Session.retrieve(session.session_id)
        if stripe_session.payment_status == 'paid' or \
            stripe_session.payment_status == 'no_payment_required':
                session.status = 'оплачен'
                session.save()
                Payment.objects.create(
                    user=user,
                    purchased_item=session.buy_object,
                    summ=stripe_session.amount_total,
                    payment_type='card'
                ).save()
        elif stripe_session.status == 'expired':
            session.status = 'просрочен'
            session.save()