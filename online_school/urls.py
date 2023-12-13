from django.urls import path
from rest_framework import routers
from online_school.views import (CourseViewSet, 
                                 LessonListAPIView, 
                                 LessonCreateAPIView, 
                                 LessonRetrieveAPIView, 
                                 LessonUpdateAPIView,
                                 LessonDestroyAPIView)
from online_school.apps import OnlineSchoolConfig

app_name = OnlineSchoolConfig.name

router = routers.DefaultRouter()
router.register(r'course', CourseViewSet, basename='course')

urlpatterns = [
    path('lesson/', LessonListAPIView.as_view(), name='lesson_list'),
    path('lesson/create/', LessonCreateAPIView.as_view(), name='lesson_create'),
    path('lesson/<int:pk>', LessonRetrieveAPIView.as_view(), name='lesson_detail'),
    path('lesson/<int:pk>/update', LessonUpdateAPIView.as_view(), name='lesson_update'),
    path('lesson/<int:pk>/delete', LessonDestroyAPIView.as_view(), name='lesson_delete'),
] + router.urls