from rest_framework.permissions import BasePermission

from online_school.models import Payment

# actions: ['list', 'create', 'retrieve', 'update', 'partial_update', 'destroy']

def is_creator(object, request):
    return object.user == request.user

def is_staff(request):
    return request.user.is_staff

def is_moderator(request):
    return request.user.groups.filter(name='Модератор').exists()

def is_su(request):
    return request.user.is_superuser


class IsStaffClass(BasePermission):
    def has_permission(self, request, view):
        return is_staff(request)


class IsCreatorClass(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True
        
    def has_object_permission(self, request, view, obj):
        if is_creator(obj, request):
            return True

class IsModeratorClass(BasePermission):
    def has_permission(self, request, view):
        return is_moderator(request)


class CourseModeratorClass(BasePermission):
    def has_permission(self, request, view):
        return view.action in \
            ['list', 'retrieve', 'update', 'partial_update'] \
                and is_moderator(request)


class IsBoughtLessonClass(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True
        
    def has_object_permission(self, request, view, obj):
        if Payment.objects.filter(user=request.user, purchased_item=obj).exists() or \
            Payment.objects.filter(user=request.user, purchased_item=obj.course).exists():
                return True


class IsBoughtCourseClass(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True
        
    def has_object_permission(self, request, view, obj):
        if view.action == 'retrieve':
            if Payment.objects.filter(user=request.user, purchased_item=obj).exists():
                return True