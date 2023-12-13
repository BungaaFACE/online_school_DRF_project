from users.apps import UsersConfig
from users.views import UserListAPIView, UserUpdateAPIView
from django.urls import path
app_name = UsersConfig.name


urlpatterns = [
    path('<int:pk>/update/', UserUpdateAPIView.as_view(), name='user_update'),
    path('', UserListAPIView.as_view(), name='user_list'),
]
