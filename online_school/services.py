from django.conf import settings
from online_school.models import CourseSubscribe
from django.core.mail import send_mail

class SendCourseUpdate:
    def __init__(self, course, message) -> None:
        
        self.mail_subject = f'Обновление курса {course.name}'
        self.message = message
        
        course_subscribes = CourseSubscribe.objects.filter(course=course)
        self.subscriber_mail_list = [sub.user.email for sub in course_subscribes]

    def send_email(self):
        send_mail(
            self.mail_subject,
            self.message,
            settings.EMAIL_HOST_USER,
            self.subscriber_mail_list,
            fail_silently=False
        )