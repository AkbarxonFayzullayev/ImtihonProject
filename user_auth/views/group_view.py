from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet

from user_auth.add_permissions import *
from user_auth.models import Group, Course
from user_auth.serializers import GroupSerializer, CourseSerializer


class GroupViewSet(ModelViewSet):
    # Guruhlar bilan CRUD amallarini bajaradi, faqat xodim va adminlarga ruxsat
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsStaffOrAdminUser]
    pagination_class = PageNumberPagination


class CourseViewSet(ModelViewSet):
    # Kurslar bilan CRUD amallarini bajaradi, faqat xodim va adminlarga ruxsat
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsStaffOrAdminUser]
    pagination_class = PageNumberPagination
