from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from user_auth.add_permissions import IsStaffOrAdminUser
from user_auth.models import User
from user_auth.serializers import UserSerializer, StaffUserSerializer


class StaffCreate(APIView):
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(request_body=StaffUserSerializer)
    def post(self, request):
        serializer = StaffUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserApi(APIView):
    permission_classes = [IsStaffOrAdminUser]

    @swagger_auto_schema(responses={200: UserSerializer(many=True)})
    def get(self, request):
        users = User.objects.all()  # Barcha foydalanuvchilarni olish
        paginator = PageNumberPagination()  # Paginatsiya ob'ektini yaratish
        paginated_users = paginator.paginate_queryset(users, request)  # Paginatsiya qo'llash

        serializer = UserSerializer(paginated_users, many=True)  # Foydalanuvchilarni serializatsiya qilish
        return paginator.get_paginated_response(serializer.data)

    @swagger_auto_schema(request_body=UserSerializer)
    def post(self, request):
        serializer = UserSerializer(data=request.date)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetail(APIView):
    permission_classes = [IsStaffOrAdminUser]

    @swagger_auto_schema(responses={200: UserSerializer()})
    def get(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        serializer = UserSerializer(user)
        return Response(data=serializer.data)

    @swagger_auto_schema(request_body=UserSerializer)
    def put(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=UserSerializer)
    def patch(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(responses={204: 'Deleted successfully', 404: 'Not Found'})
    def delete(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        user.delete()
        return Response({"detail": "User o'chirildi"}, status=204)
