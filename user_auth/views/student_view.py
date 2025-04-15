from django.contrib.auth.hashers import make_password
from rest_framework import status
from rest_framework.views import APIView

from ..models import Student
from ..models.model_teacher import *
from ..serializers import TeacherSerializer, TeacherCreateSerializer, TeacherPostSerializer, UserSerializer
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

    # def post(self,request):
    #     data = {"success":True}
    #     user = request.data["user"]
    #     student = request.data["student"]
    #     phone_number = user["phone_number"]
    #     user_serializer = UserSerializer(data=user)
    #     user["is_student"] = True
    #
    #     if user_serializer.is_valid():
    #         user_serializer.is_active = True
    #         user_serializer.password = (
    #             make_password(user_serializer.validated_data.get("password"))
    #         )
    #         user = user_serializer.save()
    #
    #         user_id = User.objects.filter(phone_number=phone_number).values("id")[0]['id']
    #         student["user"]=user_id
    #         student_serializer = StudentSerializer(data=student)
    #         if student_serializer.is_valid():
    #             student_serializer.save()
    #             data["user"] = user_serializer.data
    #             data["student"] = student_serializer.data
    #             return Response(data=data)
    #         return Response(data=student_serializer.errors)
    #     return Response(data=user_serializer.errors)
