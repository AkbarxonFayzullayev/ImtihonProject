from rest_framework.viewsets import ModelViewSet

from user_auth.models import GroupHomeWork, HomeWork, Parents, Departments, Course, Rooms, TableType, Table, Group, \
    Attendance, Lesson
from user_auth.serializers import GroupHomeWorkSerializer, HomeWorkSerializer, ParentsSerializer, DepartmentsSerializer, \
    CourseSerializer, RoomSerializer, TableTypeSerializer, TableSerializer, GroupSerializer, LessonSerializer, \
    AttendanceSerializer
from user_auth.serializers.attendance_serializer import *


class GroupHomeWorkViewSet(ModelViewSet):
    queryset = GroupHomeWork.objects.all()
    serializer_class = GroupHomeWorkSerializer

class HomeWorkViewSet(ModelViewSet):
    queryset = HomeWork.objects.all()
    serializer_class = HomeWorkSerializer

class ParentsViewSet(ModelViewSet):
    queryset = Parents.objects.all()
    serializer_class = ParentsSerializer

class DepartmentsViewSet(ModelViewSet):
    queryset = Departments.objects.all()
    serializer_class = DepartmentsSerializer

class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

class RoomsViewSet(ModelViewSet):
    queryset = Rooms.objects.all()
    serializer_class = RoomSerializer

class TableTypeViewSet(ModelViewSet):
    queryset = TableType.objects.all()
    serializer_class = TableTypeSerializer

class TableViewSet(ModelViewSet):
    queryset = Table.objects.all()
    serializer_class = TableSerializer

class GroupViewSet(ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

class AttendanceViewSet(ModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer

class TopicsViewSet(ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
