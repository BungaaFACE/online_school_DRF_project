from rest_framework import serializers

from online_school.models import Course, Lesson

class IsYoutubeLinkValidator:
    def __init__(self, field) -> None:
        self.field = field
        
    def __call__(self, value):
        if 'youtube.com' not in value.get(self.field, ''):
            raise serializers.ValidationError("Ссылка на видеоматериал должна находиться на youtube.com.")

class IsCourseOrLessonValidator:
    def __init__(self, buy_object_type, buy_object_id) -> None:
        self.buy_object_type = buy_object_type
        self.buy_object_id = buy_object_id
        
    def __call__(self, value):
        pk = value.get(self.buy_object_id)
        if value.get(self.buy_object_type) == 'lesson':
            if not Lesson.objects.filter(pk=pk).exists():
                raise serializers.ValidationError("Указанного урока не существует.")
        elif value.get(self.buy_object_type) == 'course':
            if not Course.objects.filter(pk=pk).exists():
                raise serializers.ValidationError("Указанного курса не существует.")
