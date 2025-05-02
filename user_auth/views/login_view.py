import random

from ..add_permissions import IsStaffUser
from ..make_token import *
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from django.contrib.auth.hashers import make_password
from rest_framework import status
from ..serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.cache import cache
from ..models import User
from ..serializers import SMSSerializer
from drf_yasg.utils import swagger_auto_schema


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


class RegisterUserApi(APIView):
    permission_classes = [IsAdminUser, IsStaffUser]

    @swagger_auto_schema(responses={200: UserSerializer(many=True)})
    def get(self, request):
        users = User.objects.all().order_by("-id")
        serializer = UserSerializer(users, many=True)
        return Response(data=serializer.data)

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


def send_otp():
    otp = str(random.randint(1001, 9999))
    print(otp)
    return otp


class PhoneSendOTP(APIView):
    permission_classes = [IsAuthenticated, ]

    @swagger_auto_schema(request_body=SMSSerializer)
    def post(self, request, *args, **kwargs):
        phone_number = request.data.get('phone_number')

        if not phone_number:
            return Response({
                'status': False,
            }, status=status.HTTP_400_BAD_REQUEST)

        phone = str(phone_number)
        user = User.objects.filter(phone_number__iexact=phone)
        if user.exists():
            return Response({
                'status': False,
                'detail': 'Bu telefon raqami allaqachon ro‘yxatdan o‘tgan'
            }, status=status.HTTP_400_BAD_REQUEST)
        else:
            key = send_otp()
            if key:
                cache.set(phone, key, 600)
                return Response({
                    "status": True,
                    "message": "SMS muvaffaqiyatli yuborildi"
                }, status=status.HTTP_200_OK)
            return Response({
                "status": False,
                "message": "SMS yuborishda xatolik yuz berdi"
            }, status=status.HTTP_400_BAD_REQUEST)


class VerifySMS(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=VerifySMSSerializer)
    def post(self, request):
        serializer = VerifySMSSerializer(data=request.data)

        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']
            verification_code = serializer.validated_data['verification_code']
            cached_code = str(cache.get(phone_number))

            if verification_code == cached_code:
                return Response({
                    'status': True,
                    'detail': 'OTP mos tushdi. Ro‘yxatdan o‘tishni davom ettiring.'
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'status': False,
                    'detail': 'Noto‘g‘ri tasdiqlash kodi.'
                }, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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


class AuthMeView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(responses={200: UserSerializer()})
    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
