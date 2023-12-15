from django.core.management import BaseCommand
from online_school.models import Course, Lesson


class Command(BaseCommand):
    def handle(self, *args, **options) -> str | None:

        try:
            Course.objects.all().delete()
        except:
            pass

        course_list = [
            {'name': 'course 1',
             'description': 'course 1',
             },
            {'name': 'course 2',
             'description': 'course 2',
             },
            {'name': 'course 3',
             'description': 'course 3',
             },
            {'name': 'course 4',
             'description': 'course 4',
             },
            {'name': 'course 5',
             'description': 'course 5',
             },
        ]
        
        lesson_list = [
            {'name': 'lesson 1',
             'description': 'lesson 1',
             'video_link': 'lesson_link.ru',
             },
            {'name': 'lesson 2',
             'description': 'lesson 2',
             'video_link': 'lesson_link.ru',
             },
            {'name': 'lesson 3',
             'description': 'lesson 3',
             'video_link': 'lesson_link.ru',
             },
            {'name': 'lesson 4',
             'description': 'lesson 4',
             'video_link': 'lesson_link.ru',
             },
            {'name': 'lesson 5',
             'description': 'lesson 5',
             'video_link': 'lesson_link.ru',
             },
        ]

        course_instances = []
        lesson_instances = []
        for course in course_list:
            course = Course(**course)
            course_instances.append(course)
            for lesson in lesson_list:
                lesson_instances.append(Lesson(course=course, **lesson))

        Course.objects.bulk_create(course_instances)
        Lesson.objects.bulk_create(lesson_instances)