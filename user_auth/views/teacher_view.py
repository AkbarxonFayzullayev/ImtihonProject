from django.db import transaction
from rest_framework import status
from rest_framework.views import APIView
from ..models.model_teacher import *
from ..serializers import TeacherSerializer, TeacherCreateSerializer, TeacherPostSerializer
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class Crud_Teacher(APIView):
    @swagger_auto_schema(
        responses={200: TeacherSerializer(many=True)}
    )
    def get(self, request):
        teachers = Teacher.objects.all()
        serializer = TeacherSerializer(teachers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=TeacherCreateSerializer,
    )
    def post(self, request):
        serializer = TeacherCreateSerializer(data=request.data)
        if serializer.is_valid():
            teacher = serializer.save()
            response_serializer = TeacherSerializer(teacher)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        request_body=TeacherSerializer,
    )
    def put(self, request):
        phone_number = request.data.get("phone_number")

        try:
            with transaction.atomic():
                teacher = Teacher.objects.select_related('user').get(user__phone_number=phone_number)
                user = teacher.user
                user_data = {
                    'phone_number': request.data.get('phone_number', user.phone_number),
                    'full_name': request.data.get('full_name', user.full_name),
                    'is_active': request.data.get('is_active', user.is_active)
                }
                if 'password' in request.data:
                    user.set_password(request.data['password'])
                for attr, value in user_data.items():
                    setattr(user, attr, value)
                user.save()

                serializer = TeacherSerializer(teacher, data=request.data, partial=True)
                serializer.is_valid(raise_exception=True)
                updated_teacher = serializer.save()

                if 'departments' in request.data:
                    updated_teacher.departments.set(request.data['departments'])
                if 'course' in request.data:
                    updated_teacher.course.set(request.data['course'])

                return Response(serializer.data, status=status.HTTP_200_OK)

        except Teacher.DoesNotExist:
            return Response({"detail": "O'qituvchi topilmadi"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        phone_number = request.data.get("phone_number")

        try:
            with transaction.atomic():
                teacher = Teacher.objects.select_related('user').get(user__phone_number=phone_number)
                user = teacher.user

                teacher.delete()
                user.delete()

                return Response(
                    {"detail": "Success" },
                    status=status.HTTP_204_NO_CONTENT
                )
        except Teacher.DoesNotExist:
            return Response(
                {"detail": "O'qituvchi topilmadi"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"detail": f"O'chirib bo'lmadi: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST
            )

class Teacher_Api(APIView):
    @swagger_auto_schema(
        responses={200: TeacherSerializer(many=True)}
    )
    def get(self,request):
        teachers = Teacher.objects.all()
        serializer = TeacherSerializer(teachers,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=TeacherPostSerializer
    )
    def post(self,request):
        serializer = TeacherPostSerializer(data=request.data)
        if serializer.is_valid():
            teacher = serializer.save()
            response_serializer = TeacherSerializer(teacher)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
