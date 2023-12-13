from rest_framework import serializers
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('phone', 'avatar', 'city')
        
        
class UserSerializerPkMail(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('pk', 'mail', 'phone', 'avatar', 'city')
