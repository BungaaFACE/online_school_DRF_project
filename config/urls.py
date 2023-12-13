from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('online-school/', include('online_school.urls', namespace='online_school')),
    path('users/', include('users.urls', namespace='users')),
]
