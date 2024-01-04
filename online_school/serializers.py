from rest_framework import serializers
from online_school.models import Course, CourseSubscribe, Lesson, Payment, StripeSession
from online_school.permissions import CourseModeratorClass, IsModeratorClass
from rest_framework.permissions import IsAuthenticated
from online_school.validators import IsCourseOrLessonValidator, IsYoutubeLinkValidator


class LessonSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Lesson
        fields = '__all__'
        validators = [IsYoutubeLinkValidator(field='video_link')]


class CourseSerializer(serializers.ModelSerializer):
    lessons_count = serializers.IntegerField(source='lesson_set.all.count', read_only=True)
    lessons = LessonSerializer(source='lesson_set', read_only=True, many=True)
    is_subscribed = serializers.SerializerMethodField(read_only=True)

    def get_is_subscribed(self, obj):
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user
            return obj.course_sub.filter(user=user).exists()
        return False


    class Meta:
        model = Course
        fields = '__all__'


class PaymentSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Payment
        fields = '__all__'
        
        
class CourseSubscribeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = CourseSubscribe
        fields = ['course']

class BuySerializer(serializers.Serializer):
    buy_object_type = serializers.CharField(required=False)
    buy_object_id = serializers.IntegerField()

    class Meta:
        fields = ['buy_object_id']
        validators = [
            IsCourseOrLessonValidator(
                buy_object_type='buy_object_type',
                buy_object_id='buy_object_id')
        ]


class StripeSessionSerializer(serializers.ModelSerializer):
    buy_object_type = serializers.SerializerMethodField()
    buy_object_name = serializers.SerializerMethodField()
    
    def get_buy_object_type(self, obj):
        model_name = obj.buy_object.__class__.__name__
        print(model_name)
        if 'Course' in model_name:
            return 'Курс'
        elif 'Lesson' in model_name:
            return 'Урок'
    
    def get_buy_object_name(self, obj):
        return obj.buy_object.name

    class Meta:
        model = StripeSession
        fields = ['buy_object_type', 'buy_object_name', 'status']
        read_only = '__all__'