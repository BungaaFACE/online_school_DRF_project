from rest_framework import generics
from users.models import User
from users.serializers import UserSerializerPrivateUpdate, UserSerializerPublic, UserSerializerPrivateDetails
from rest_framework.permissions import IsAuthenticated

class UserUpdateAPIView(generics.UpdateAPIView):
    serializer_class = UserSerializerPrivateUpdate
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return User.objects.get(user=self.request.user)
    
class UserListAPIView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializerPublic
    permission_classes = [IsAuthenticated]


class UserRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = UserSerializerPrivateDetails
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.get_object() == self.request.user:
            return UserSerializerPrivateDetails
        else:
            return UserSerializerPublic
    
    def get_object(self):
        pk = self.kwargs.get('pk', self.request.user.pk)
        return User.objects.get(pk=pk)