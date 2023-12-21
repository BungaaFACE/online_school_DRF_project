from rest_framework import serializers
from users.models import User
from online_school.serializers import PaymentSerializer


class UserSerializerPrivateUpdate(serializers.ModelSerializer):
    user_payments = PaymentSerializer(source='payment_set', read_only=True, many=True)
    
    class Meta:
        model = User
        exclude = ['password', 'is_superuser', 'is_staff', 'email', 'is_active', 'groups', 'user_permissions']


class UserSerializerPrivateDetails(serializers.ModelSerializer):
    user_payments = PaymentSerializer(source='payment_set', read_only=True, many=True)
    
    class Meta:
        model = User
        fields = '__all__'
        
        
class UserSerializerPublic(serializers.ModelSerializer):

    class Meta:
        model = User
        exclude = ('password', 'last_name')
        
