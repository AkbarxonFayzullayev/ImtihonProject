from django.contrib.auth.hashers import make_password
from rest_framework import status
from rest_framework.views import APIView

from ..models import Student
from ..models.model_teacher import *
from ..serializers import TeacherSerializer,  TeacherPostSerializer, UserSerializer
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from ..serializers.student_serilalizer import StudentSerializer, StudentPostSerializer


class Student_Api(APIView):
    @swagger_auto_schema(
        responses={200: StudentSerializer(many=True)}
    )
    def get(self,request):
        students = Student.objects.all()
        serializer = StudentSerializer(students,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=StudentPostSerializer
    )
    def post(self,request):
        serializer = StudentPostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        return Response(data=serializer.errors)
