from django.contrib.auth.hashers import make_password
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.views import APIView

from ..models import Student
from ..models.model_teacher import *
from ..serializers import TeacherSerializer, TeacherPostSerializer, UserSerializer
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from ..serializers.student_serilalizer import StudentSerializer, StudentPostSerializer


class Student_Api(APIView):
    @swagger_auto_schema(
        responses={200: StudentSerializer(many=True)}
    )
    def get(self, request):
        students = Student.objects.all()
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=StudentPostSerializer
    )
    def post(self, request):
        serializer = StudentPostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        return Response(data=serializer.errors)


class StudentDetail(APIView):
    @swagger_auto_schema(responses={200: StudentPostSerializer()})
    def get(self, request, pk):
        student = get_object_or_404(Student, pk=pk)
        serializer = StudentSerializer(student)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=StudentPostSerializer)
    def put(self, request, pk):
        student = get_object_or_404(Student, pk=pk)
        serializer = StudentPostSerializer(student, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=StudentPostSerializer)
    def patch(self, request, pk):
        student = get_object_or_404(Student, pk=pk)
        serializer = StudentPostSerializer(student, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Delete student by ID",
        responses={204: 'Deleted successfully', 404: 'Not Found'})
    def delete(self, request, pk):
        try:
            student = Student.objects.get(pk=pk)
        except Student.DoesNotExist:
            raise NotFound("Bunday ID ga ega Teacher topilmadi. ")
        student.user.delete()
        student.delete()
        return Response({"detail": "Teacher va unga tegishli User o'chirildi"}, status=204)
