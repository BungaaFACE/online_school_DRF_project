from rest_framework import serializers

class IsYoutubeLinkValidator:
    def __init__(self, field) -> None:
        self.field = field
        
    def __call__(self, value):
        if 'youtube.com' not in value.get(self.field, ''):
            raise serializers.ValidationError("Ссылка на видеоматериал должна находиться на youtube.com.")
