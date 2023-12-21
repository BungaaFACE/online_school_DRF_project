from django.shortcuts import render
from rest_framework import viewsets, generics
from online_school.permissions import CourseModeratorClass, IsCreatorClass, IsModeratorClass, is_moderator, is_su
from rest_framework.permissions import IsAuthenticated
from online_school.serializers import CourseSerializer, LessonSerializer, PaymentSerializer
from online_school.models import Course, Lesson, Payment
from django_filters import rest_framework as filters

class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    permission_classes = [CourseModeratorClass|IsAuthenticated&~IsModeratorClass]
    
    def perform_create(self, serializer):
        data = serializer.save()
        data.user = self.request.user
        data.save()
    
    def get_queryset(self):
        if is_moderator(self.request) or is_su(self.request):
            return Course.objects.all()
        return Course.objects.filter(user=self.request.user)


class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    
    def get_queryset(self):
        if is_moderator(self.request) or is_su(self.request):
            return Course.objects.all()
        return Course.objects.filter(user=self.request.user)

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


class LessonUpdateAPIView(generics.UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsModeratorClass|IsAuthenticated&IsCreatorClass]
    
class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated&IsCreatorClass&~IsModeratorClass]

class PaymentViewSet(viewsets.ModelViewSet):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    filterset_fields = ('course__name', 'lesson__name', 'payment_type') # Набор полей для фильтрации
    ordering_fields = ('date',)