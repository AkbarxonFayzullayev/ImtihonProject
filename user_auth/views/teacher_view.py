from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from user_auth.add_permissions import IsTeacherUser, IsStaffOrAdminUser
from ..models import Group
from ..models.model_teacher import *
from ..serializers import TeacherSerializer, TeacherPostSerializer, DepartmentsSerializer
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema


class Teacher_Api(APIView):
    permission_classes = [IsStaffOrAdminUser]

    @swagger_auto_schema(
        responses={200: TeacherSerializer(many=True)}
    )
    def get(self, request):
        teachers = Teacher.objects.all()  # Barcha o'qituvchilarni olish
        serializer = TeacherSerializer(teachers, many=True)  # Serializatsiya
        return Response(serializer.data)

    @swagger_auto_schema(request_body=TeacherPostSerializer)
    def post(self, request):
        serializer = TeacherPostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TeacherDetail(APIView):
    permission_classes = [IsStaffOrAdminUser]

    @swagger_auto_schema(responses={200: TeacherPostSerializer()})
    def get(self, request, pk):
        teacher = get_object_or_404(Teacher, pk=pk)
        serializer = TeacherPostSerializer(teacher)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=TeacherPostSerializer)
    def put(self, request, pk):
        teacher = get_object_or_404(Teacher, pk=pk)
        serializer = TeacherPostSerializer(teacher, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=TeacherPostSerializer)
    def patch(self, request, pk):
        teacher = get_object_or_404(Teacher, pk=pk)
        serializer = TeacherPostSerializer(teacher, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(responses={204: 'Deleted successfully', 404: 'Not Found'})
    def delete(self, request, pk):
        try:
            teacher = Teacher.objects.get(pk=pk)
        except Teacher.DoesNotExist:
            raise NotFound("Bunday ID ga ega Teacher topilmadi. ")
        teacher.user.delete()
        teacher.delete()
        return Response({"detail": "Teacher va unga tegishli User o'chirildi"}, status=204)


class DepartmentsViewSet(ModelViewSet):
    queryset = Departments.objects.all()
    serializer_class = DepartmentsSerializer
    permission_classes = [IsStaffOrAdminUser]
    pagination_class = PageNumberPagination


class TeacherGetGroups(APIView):
    permission_classes = [IsTeacherUser]

    def get(self, request):
        user = request.user
        teacher = Teacher.objects.get(user=user)
        groups = Group.objects.filter(teacher=teacher)

        response = []
        for group in groups:
            response.append({
                "id": group.id,
                "title": group.title,
                "start_date": group.start_date,
                "end_date": group.end_date,
                "course": group.course.title if group.course else None,
                "student_count": group.students.count()
            })

        return Response(response)


class TeacherGetGroupStudents(APIView):
    permission_classes = [IsTeacherUser]

    def get(self, request):
        user = request.user
        teacher = get_object_or_404(Teacher, user=user)
        groups = Group.objects.filter(teacher=teacher)

        response = []
        for group in groups:
            students_data = []
            for student in group.students.all():
                students_data.append({
                    "id": student.id,
                    "fullname": student.fullname,
                    "phone_number": student.user.phone_number
                })

            response.append({
                "id": group.id,
                "title": group.title,
                "student_count": group.students.count(),
                "students": students_data
            })

        return Response(response)
