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


# StaffCreate, yangi xodim (staff user) yaratish uchun API
class StaffCreate(APIView):
    permission_classes = [IsAdminUser]  # Faqat admin foydalanuvchilariga ruxsat

    # Yangi xodim yaratish
    @swagger_auto_schema(request_body=StaffUserSerializer)
    def post(self, request):
        serializer = StaffUserSerializer(data=request.data)  # Ma'lumotlarni serializerga uzatish
        if serializer.is_valid():
            serializer.save()  # Yangi xodimni saqlash
            return Response(data=serializer.data)  # Yaratilgan xodim ma'lumotlarini qaytarish
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # Xatolik yuz berdi


# UserApi, foydalanuvchilarni boshqarish uchun API
class UserApi(APIView):
    permission_classes = [IsStaffOrAdminUser]  # Faqat staff yoki admin foydalanuvchilariga ruxsat

    # Barcha foydalanuvchilarni olish
    @swagger_auto_schema(responses={200: UserSerializer(many=True)})
    def get(self, request):
        users = User.objects.all()  # Barcha foydalanuvchilarni olish
        paginator = PageNumberPagination()  # Paginatsiya ob'ektini yaratish
        paginated_users = paginator.paginate_queryset(users, request)  # Foydalanuvchilarni sahifalash

        serializer = UserSerializer(paginated_users, many=True)  # Foydalanuvchilarni serializatsiya qilish
        return paginator.get_paginated_response(serializer.data)  # Sahifalangan javobni qaytarish

    # Yangi foydalanuvchi yaratish
    @swagger_auto_schema(request_body=UserSerializer)
    def post(self, request):
        serializer = UserSerializer(data=request.data)  # Ma'lumotlarni serializerga uzatish
        if serializer.is_valid():
            serializer.save()  # Yangi foydalanuvchini saqlash
            return Response(data=serializer.data)  # Yaratilgan foydalanuvchi ma'lumotlarini qaytarish
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # Xatolik yuz berdi


# UserDetail, ma'lum bir foydalanuvchining ma'lumotlarini olish, yangilash va o'chirish uchun API
class UserDetail(APIView):
    permission_classes = [IsStaffOrAdminUser]  # Faqat staff yoki admin foydalanuvchilariga ruxsat

    # Foydalanuvchining ma'lumotlarini olish
    @swagger_auto_schema(responses={200: UserSerializer()})
    def get(self, request, pk):
        user = get_object_or_404(User, pk=pk)  # ID bo'yicha foydalanuvchini olish
        serializer = UserSerializer(user)  # Foydalanuvchini serializatsiya qilish
        return Response(data=serializer.data)  # Foydalanuvchining ma'lumotlarini qaytarish

    # Foydalanuvchini to'liq yangilash
    @swagger_auto_schema(request_body=UserSerializer)
    def put(self, request, pk):
        user = get_object_or_404(User, pk=pk)  # ID bo'yicha foydalanuvchini olish
        serializer = UserSerializer(user, data=request.data)  # Yangilash uchun ma'lumot
        if serializer.is_valid():
            serializer.save()  # Foydalanuvchini yangilash
            return Response(data=serializer.data)  # Yangilangan foydalanuvchi ma'lumotlarini qaytarish
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # Xatolik yuz berdi

    # Foydalanuvchini qisman yangilash
    @swagger_auto_schema(request_body=UserSerializer)
    def patch(self, request, pk):
        user = get_object_or_404(User, pk=pk)  # ID bo'yicha foydalanuvchini olish
        serializer = UserSerializer(user, data=request.data, partial=True)  # Qisman yangilash
        if serializer.is_valid():
            serializer.save()  # Foydalanuvchini qisman yangilash
            return Response(data=serializer.data)  # Yangilangan foydalanuvchi ma'lumotlarini qaytarish
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # Xatolik yuz berdi

    # Foydalanuvchini o'chirish
    @swagger_auto_schema(responses={204: 'Deleted successfully', 404: 'Not Found'})
    def delete(self, request, pk):
        user = get_object_or_404(User, pk=pk)  # ID bo'yicha foydalanuvchini olish
        user.delete()  # Foydalanuvchini o'chirish
        return Response({"detail": "User o'chirildi"}, status=204)  # Foydalanuvchi muvaffaqiyatli o'chirildi
