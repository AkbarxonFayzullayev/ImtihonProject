import random

from ..add_permissions import IsStaffOrAdminUser
from ..make_token import *
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth.hashers import make_password
from rest_framework import status
from ..serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.cache import cache
from ..models import User
from ..serializers import SMSSerializer
from drf_yasg.utils import swagger_auto_schema


# Login API — foydalanuvchiga JWT token qaytaradi
class LoginApi(APIView):
    permission_classes = [AllowAny, ]

    @swagger_auto_schema(request_body=LoginSerializer)
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data.get("user")
            token = get_tokens_for_user(user)
            token["is_admin"] = user.is_superuser
        return Response(data=token, status=status.HTTP_200_OK)


# Foydalanuvchilarni ro'yxatdan o'tkazish va ko'rish
class RegisterUserApi(APIView):
    permission_classes = [IsStaffOrAdminUser]

    # Barcha foydalanuvchilarni ko‘rish
    @swagger_auto_schema(responses={200: UserSerializer(many=True)})
    def get(self, request):
        users = User.objects.all().order_by("-id")
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    # Yangi foydalanuvchi yaratish
    @swagger_auto_schema(request_body=UserSerializer)
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            password = serializer.validated_data.get('password')
            serializer.validated_data['password'] = make_password(password)
            serializer.save()
            return Response({
                "status": True,
                'datail': 'account create'
            })


# Authenticated foydalanuvchi parolini sozlash
class SetPasswordView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=SetPasswordSerializer)
    def post(self, request):
        serializer = SetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            new_password = serializer.validated_data['new_password']
            user = request.user
            user.set_password(new_password)
            user.save()
            return Response({"detail": "Parol muvaffaqiyatli yangilandi"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Foydalanuvchi eski parol bilan yangilash
class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated, ]

    @swagger_auto_schema(request_body=ChangePasswordSerializer)
    def patch(self, request):
        serializer = ChangePasswordSerializer(instance=self.request.user, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"data": serializer.data,
                             "message": "Changed your password successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 4 xonali OTP kod generatsiyasi
def generate_otp():
    otp = str(random.randint(1000, 9999))
    print(f"Generated OTP: {otp}")
    return otp


# Telefon raqamga OTP yuborish (SMS emas, faqat test uchun kod qaytadi)
class PhoneSendOTP(APIView):
    # permission_classes = [IsAuthenticated, ]

    @swagger_auto_schema(request_body=SMSSerializer)
    def post(self, request, *args, **kwargs):
        phone_number = request.data.get('phone_number')

        if not phone_number:
            return Response({
                'status': False,
            }, status=status.HTTP_400_BAD_REQUEST)

        phone = str(phone_number)
        user = User.objects.filter(phone_number=phone).first()
        if user:
            otp = generate_otp()
            cache.set(phone, otp, 600)  # 10 daqiqa amal qiladi
            return Response({
                "status": True,
                "message": "Tasdiqlash kodi yuborildi",
                "code": otp
            }, status=status.HTTP_200_OK)
        return Response({
            'status': False,
            'message': 'Telefon raqami tizimda mavjud emas'
        }, status=status.HTTP_400_BAD_REQUEST)


# Parolni tiklash uchun (OTP va yangi parol kiritiladi)
class ResetPassword(APIView):
    # permission_classes = [IsAuthenticated, ]

    @swagger_auto_schema(request_body=VerifySMSSerializer)
    def post(self, request):
        serializer = VerifySMSSerializer(data=request.data)

        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']
            verification_code = serializer.validated_data['verification_code']
            new_password = serializer.validated_data['new_password']
            renew_password = serializer.validated_data['renew_password']

            # Keshdagi OTP ni tekshirish
            cached_otp = cache.get(phone_number)

            if cached_otp != verification_code:
                return Response({
                    'status': False,
                    'message': 'Noto‘g‘ri tasdiqlash kodi'
                }, status=status.HTTP_400_BAD_REQUEST)

            # Parollar bir xilmi?
            if new_password != renew_password:
                return Response({
                    'status': False,
                    'message': 'Parollar mos kelmaydi'
                }, status=status.HTTP_400_BAD_REQUEST)

            # Parolni yangilash
            user = User.objects.filter(phone_number=phone_number).first()
            if user:
                user.set_password(new_password)
                user.save()

                # Keshdan OTP ni o‘chirish
                cache.delete(phone_number)

                return Response({
                    'status': True,
                    'message': 'Parol muvaffaqiyatli yangilandi'
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'status': False,
                    'message': 'Foydalanuvchi topilmadi'
                }, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Foydalanuvchi logout qiladi (refresh token black list ga qo‘shiladi)
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=RefreshTokenSerializer)
    def post(self, request):
        serializer = RefreshTokenSerializer(data=request.data)
        if serializer.is_valid():
            refresh_token = serializer.validated_data["refresh"]
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()
                return Response({"detail": "Successfully logged out."}, status=status.HTTP_200_OK)
            except Exception:
                return Response({"error": "Invalid refresh token."}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Joriy foydalanuvchi ma'lumotlarini olish (profil)
class AuthMeView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(responses={200: UserSerializer()})
    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
