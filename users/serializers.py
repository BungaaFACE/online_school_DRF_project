from rest_framework import serializers
from users.models import User
from online_school.serializers import PaymentSerializer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('phone', 'avatar', 'city')
        
        
class UserSerializerPkMail(serializers.ModelSerializer):
    user_payments = PaymentSerializer(source='payment_set', read_only=True, many=True)
    
    class Meta:
        model = User
        fields = ('pk', 'email', 'phone', 'avatar', 'city', 'user_payments')
