from django.contrib.auth.hashers import make_password
from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.views import APIView

from ..models import User
from ..models.model_teacher import *
from ..serializers import TeacherSerializer, TeacherPostSerializer, UserSerializer
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class Teacher_Api(APIView):
    @swagger_auto_schema(
        responses={200: TeacherSerializer(many=True)}
    )
    def get(self, request):
        teachers = Teacher.objects.all()
        serializer = TeacherSerializer(teachers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=TeacherPostSerializer
    )
    def post(self, request):
        serializer = TeacherPostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TeacherDetail(APIView):
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

    @swagger_auto_schema(
        operation_description="Delete student by ID",
        responses={204: 'Deleted successfully', 404: 'Not Found'})
    def delete(self, request, pk):
        try:
            teacher = Teacher.objects.get(pk=pk)
        except Teacher.DoesNotExist:
            raise NotFound("Bunday ID ga ega Teacher topilmadi. ")
        teacher.user.delete()
        teacher.delete()
        return Response({"detail": "Teacher va unga tegishli User o'chirildi"}, status=204)
