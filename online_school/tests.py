from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from online_school.models import Course, CourseSubscribe, Lesson
from users.models import User
from rest_framework_simplejwt.tokens import RefreshToken


class LessonTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(
            email='test@gmail.com',
            first_name='user1',
            last_name='user1',
            is_active=True,
            is_staff=False,
            is_superuser=False,
        )
        self.user.set_password('user')
        self.user.save()
        
        self.access_token = str(RefreshToken.for_user(self.user).access_token)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        
        self.course = Course.objects.create(
            name = 'Course 1',
            user = self.user
        )
        
        self.lesson = Lesson.objects.create(
            course = self.course,
            name = 'lesson1',
            video_link = 'youtube.com/awadad1',
            user = self.user)
        
        # sub = CourseSubscribe.objects.create(
        #     user=self.user,
        #     course=self.course
        # )
        # sub.save()
        
    def test_create_lesson(self):
        data = {
            'course': self.course.pk,
            'name': 'lesson2',
            'video_link': 'youtube.com/awadad'
            }
        
        response = self.client.post('/online-school/lesson/create/', 
                                    data=data,
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_lessons(self):
        # Тестирование GET-запроса к API
        response = self.client.get('/online-school/lesson/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(response.json(), {})

    def test_update_lesson(self):
        update_data = {
            'course': self.course.pk,
            'name': 'lesson11',
            'video_link': 'youtube.com/awadad11'
            }
        response = self.client.patch(
            f'/online-school/lesson/{self.lesson.pk}/update/', 
            data=update_data,
            format='json'
            )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_destroy_lesson(self):
        response = self.client.delete(f'/online-school/lesson/{str(self.lesson.pk)}/delete/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)