from rest_framework import serializers
from online_school.models import Course, CourseSubscribe, Lesson, Payment
from online_school.permissions import CourseModeratorClass, IsModeratorClass
from rest_framework.permissions import IsAuthenticated
from online_school.validators import IsYoutubeLinkValidator


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
