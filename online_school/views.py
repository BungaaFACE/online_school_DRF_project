from django.shortcuts import render
from rest_framework import viewsets, generics, status, views
from rest_framework.response import Response
from online_school.pagination import PagintaionThreeTen
from online_school.permissions import CourseModeratorClass, IsCreatorClass, IsModeratorClass, is_moderator, is_su
from rest_framework.permissions import IsAuthenticated
from online_school.serializers import BuySerializer, CourseSerializer, CourseSubscribeSerializer, LessonSerializer, PaymentSerializer, StripeSessionSerializer
from online_school.models import Course, CourseSubscribe, Lesson, Payment, StripeSession
from django_filters import rest_framework as filters
from django.shortcuts import get_object_or_404
from django.urls import reverse
import stripe
import time

from online_school.services import SendCourseUpdate, update_stripe_sessions_status

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
                         f'В курс {data.course.name} был добавлен урок {data.name}.').send_email.delay()


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
                    f'В курсе {data.course.name} был изменен урок {data.name}.').send_email.delay()

    
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
                    f'В курсе {instance.course.name} был удален урок {instance.name}.').send_email.delay()
        
    

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


class BuyAPIView(generics.RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = BuySerializer
    permission_classes = [IsAuthenticated]
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

class BuyAPIView(generics.CreateAPIView):
    queryset = StripeSession.objects.all()
    serializer_class = BuySerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        # Дополняем сериализатор для корректной валидации существования продукта
        if 'lesson' in request.get_full_path():
            serializer.buy_object_type = 'lesson'
        elif 'course' in request.get_full_path():
            serializer.buy_object_type = 'course'
        serializer.is_valid(raise_exception=True)
        
        # Получаем объект и его данные
        buy_object_pk = serializer.validated_data['buy_object_id']
        if 'lesson' in request.get_full_path():
            buy_object = Lesson.objects.get(pk=buy_object_pk)
            name = f'Lesson {buy_object.name}'
        elif 'course' in request.get_full_path():
            buy_object = Course.objects.get(pk=buy_object_pk)
            name = f'Course {buy_object.name}'
        price = buy_object.price
        
        # Создание ценника
        stripe_price = stripe.Price.create(
            currency="rub",
            unit_amount=price*100,
            product_data={"name": name},
        )
        # Создание сессии для оплаты
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price': stripe_price.id,
                    'quantity': 1,
                },
            ],
            mode="payment",
            # 30 минут с небольшим запасом
            expires_at= int(time.time()) + 1830,
            success_url=request.build_absolute_uri(reverse('online_school:stripe_status')),
        )
        # Логи сессий для дальнейшей проверки факта оплаты
        StripeSession.objects.create(
            session_id=session.id,
            user=self.request.user,
            buy_object=buy_object
        ).save()
        return Response({'detail': 'Ссылка на оплату', 'checkout_url': session.url}, status=status.HTTP_201_CREATED)


class GetPaymentView(views.APIView):
    serializer_class = StripeSessionSerializer
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        # Обновление статуса сессий пользователя
        update_stripe_sessions_status(request.user)
        
        # Вывод списка сессий пользователя
        queryset = StripeSession.objects.filter(user=request.user)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)