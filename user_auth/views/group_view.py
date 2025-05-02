from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ModelViewSet

from user_auth.add_permissions import IsStaffUser
from user_auth.models import Group, Course
from user_auth.serializers import GroupSerializer, CourseSerializer


class GroupViewSet(ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAdminUser, IsStaffUser]

class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAdminUser,IsStaffUser]