from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

schema_view = get_schema_view(
   openapi.Info(
      title="Онлайн школа DRF",
      default_version='v1',
      description="Онлайн школа DRF",
      terms_of_service="Пока нет",
      contact=openapi.Contact(email="github.com/bungaaface"),
      license=openapi.License(name="Пока нет"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('online-school/', include('online_school.urls', namespace='online_school')),
    path('users/', include('users.urls', namespace='users')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
