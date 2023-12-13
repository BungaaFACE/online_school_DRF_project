from rest_framework import generics
from users.models import User
from users.serializers import UserSerializer, UserSerializerPkMail

class UserUpdateAPIView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
class UserListAPIView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializerPkMail