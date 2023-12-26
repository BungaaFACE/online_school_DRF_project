from django.shortcuts import render
from rest_framework import viewsets, generics
from online_school.pagination import PagintaionThreeTen
from online_school.permissions import CourseModeratorClass, IsCreatorClass, IsModeratorClass, is_moderator, is_su
from rest_framework.permissions import IsAuthenticated
from online_school.serializers import CourseSerializer, CourseSubscribeSerializer, LessonSerializer, PaymentSerializer
from online_school.models import Course, CourseSubscribe, Lesson, Payment
from django_filters import rest_framework as filters
from django.shortcuts import get_object_or_404

from online_school.services import SendCourseUpdate

class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    permission_classes = [CourseModeratorClass|IsAuthenticated&~IsModeratorClass]
    pagination_class = PagintaionThreeTen
    
    def perform_create(self, serializer):
        data = serializer.save()
        data.user = self.request.user
        data.save()
    
    def get_queryset(self):
        if is_moderator(self.request) or is_su(self.request):
            return Course.objects.all().order_by('name')
        return Course.objects.filter(user=self.request.user).order_by('name')


class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    pagination_class = PagintaionThreeTen
    
    def get_queryset(self):
        if is_moderator(self.request) or is_su(self.request):
            return Lesson.objects.all().order_by('name')
        return Lesson.objects.filter(user=self.request.user).order_by('name')

class LessonRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsModeratorClass|IsAuthenticated&IsCreatorClass]
    
    

class LessonCreateAPIView(generics.CreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated&~IsModeratorClass]
    
    def perform_create(self, serializer):
        data = serializer.save()
        data.user = self.request.user
        data.save()
        SendCourseUpdate(data.course, 
                         f'В курс {data.course.name} был добавлен урок {data.name}.').send_email()


class LessonUpdateAPIView(generics.UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsModeratorClass|IsAuthenticated&IsCreatorClass]
    
    def get_object(self):
        if self.kwargs.get('pk'):
            return self.get_queryset().get(pk=self.kwargs['pk'])
        return super().get_object()

    def perform_update(self, serializer):
        super().perform_update(serializer)
        data = serializer.save()
        SendCourseUpdate(data.course, 
                    f'В курсе {data.course.name} был изменен урок {data.name}.').send_email()

    
class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated&IsCreatorClass&~IsModeratorClass]
    
    def get_object(self):
        if self.kwargs.get('pk'):
            return self.get_queryset().get(pk=self.kwargs['pk'])
        return super().get_object()
    
    def perform_destroy(self, instance):
        super().perform_destroy(instance)
        SendCourseUpdate(instance.course, 
                    f'В курсе {instance.course.name} был удален урок {instance.name}.').send_email()
        
    

class PaymentViewSet(viewsets.ModelViewSet):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    filterset_fields = ('course__name', 'lesson__name', 'payment_type') # Набор полей для фильтрации
    ordering_fields = ('date',)


class CourseSubscribeCreateAPIView(generics.CreateAPIView):
    serializer_class = CourseSubscribeSerializer
    queryset = CourseSubscribe.objects.all()
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CourseSubscribeDestroyAPIView(generics.DestroyAPIView):
    serializer_class = CourseSubscribeSerializer
    queryset = CourseSubscribe.objects.all()
    permission_classes = [IsAuthenticated]
    
    def perform_destroy(self, instance):
        instance.user = self.request.user
        instance.delete()


class CourseSubscribeListAPIView(generics.ListAPIView):
    serializer_class = CourseSubscribeSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return CourseSubscribe.objects.filter(user=self.request.user)
