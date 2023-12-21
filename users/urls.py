from users.apps import UsersConfig
from users.views import UserListAPIView, UserRetrieveAPIView, UserUpdateAPIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.urls import path
app_name = UsersConfig.name


urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('<int:pk>/update/', UserUpdateAPIView.as_view(), name='user_update'),
    path('details/<int:pk>/', UserRetrieveAPIView.as_view(), name='user_detail_pk'),
    path('details/', UserRetrieveAPIView.as_view(), name='user_detail'),
    path('', UserListAPIView.as_view(), name='user_list'),
]
