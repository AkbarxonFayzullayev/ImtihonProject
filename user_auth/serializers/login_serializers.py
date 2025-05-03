from django.contrib.auth import authenticate
from rest_framework import serializers

from ..models import *


# LoginSerializer - Foydalanuvchi tizimga kirishi uchun autentifikatsiya qiluvchi serializer
class LoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField()  # Telefon raqam
    password = serializers.CharField()  # Parol

    def validate(self, attrs):
        phone_number = attrs.get("phone_number")
        password = attrs.get("password")

        # Foydalanuvchini telefon raqamiga qarab qidirish
        try:
            user = User.objects.get(phone_number=phone_number)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                {"success": False, "detail": "User topilmadi"})  # Agar foydalanuvchi topilmasa, xato

        # Parolni tekshirish
        auth_user = authenticate(phone_number=user.phone_number, password=password)
        if auth_user is None:
            raise serializers.ValidationError({"success": False,
                                               "detail": "phone_number yoki password xato"})  # Agar autentifikatsiya muvaffaqiyatsiz bo'lsa
        attrs["user"] = auth_user  # Muvoffaqiyatli foydalanuvchi autentifikatsiyasi
        return attrs


# UserSerializer - Foydalanuvchi modelini serializatsiya qilish
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User  # Foydalanuvchi modeli
        fields = ('id', 'phone_number', 'password', 'is_active', 'is_staff', "is_teacher", 'is_admin',
                  'is_student')  # Kerakli maydonlar


# StaffUserSerializer - Foydalanuvchining xodim sifatida serializatsiya qilish
class StaffUserSerializer(serializers.ModelSerializer):
    is_active = serializers.BooleanField(read_only=True)  # Foydalanuvchi faoliyatini faqat o'qish
    is_staff = serializers.BooleanField(read_only=True)  # Xodim holatini faqat o'qish
    is_teacher = serializers.BooleanField(read_only=True)  # O'qituvchi holatini faqat o'qish
    is_admin = serializers.BooleanField(read_only=True)  # Admin holatini faqat o'qish
    is_student = serializers.BooleanField(read_only=True)  # Talaba holatini faqat o'qish

    class Meta:
        model = User  # Foydalanuvchi modeli
        fields = ('id', 'phone_number', 'password', 'is_active', 'is_staff', "is_teacher", 'is_admin',
                  'is_student')  # Kerakli maydonlar

    def create(self, validated_data):
        validated_data['is_active'] = True  # Yangi foydalanuvchi faol
        validated_data['is_staff'] = True  # Xodim sifatida yaratish
        user = User.objects.create_user(**validated_data)  # Yangi foydalanuvchi yaratish
        return user


# ChangePasswordSerializer - Foydalanuvchining parolini o'zgartirish uchun serializer
class ChangePasswordSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(required=True, write_only=True)  # Eski parol
    new_password = serializers.CharField(required=True, write_only=True)  # Yangi parol
    re_new_password = serializers.CharField(required=True, write_only=True)  # Yangi parolni tasdiqlash

    def update(self, instance, validated_data):
        # Eski parolni tekshirish
        if not validated_data['old_password']:
            raise serializers.ValidationError({'old_password': 'old_password kiritilishi shart'})

        if not instance.check_password(validated_data['old_password']):  # Eski parolni tekshirish
            raise serializers.ValidationError({'old_password': 'old_password xato'})

        # Yangi parol va tasdiq parolini solishtirish
        if validated_data['new_password'] != validated_data['re_new_password']:
            raise serializers.ValidationError(
                {'passwords': "new_password va renew_password bir biriga teng bo'lishi kerak"})

        if validated_data['new_password'] == validated_data['re_new_password'] and instance.check_password(
                validated_data['old_password']):
            instance.set_password(validated_data['new_password'])  # Yangi parolni qo'llash
            instance.save()  # O'zgarishlarni saqlash
            return instance

    class Meta:
        model = User  # Foydalanuvchi modeli
        fields = ['old_password', 'new_password', 're_new_password']  # Kerakli maydonlar


# SetPasswordSerializer - Parolni o'rnatish uchun serializer (masalan, parolni tiklashda)
class SetPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(write_only=True)  # Yangi parol
    confirm_password = serializers.CharField(write_only=True)  # Parolni tasdiqlash

    def validate(self, data):
        if data['new_password'] != data['confirm_password']:  # Parollar mos kelmasligi
            raise serializers.ValidationError("Parollar mos emas.")
        return data


# SMSSerializer - SMS yuborish uchun telefon raqamini qabul qiladigan serializer
class SMSSerializer(serializers.Serializer):
    phone_number = serializers.CharField()  # Telefon raqami


# VerifySMSSerializer - SMS tasdiqlash kodi va yangi parolni tasdiqlash uchun serializer
class VerifySMSSerializer(serializers.Serializer):
    phone_number = serializers.CharField()  # Telefon raqami
    verification_code = serializers.CharField()  # SMS tasdiqlash kodi
    new_password = serializers.CharField()  # Yangi parol
    renew_password = serializers.CharField()  # Parolni tasdiqlash


# RefreshTokenSerializer - Tokenni yangilash uchun serializer
class RefreshTokenSerializer(serializers.Serializer):
    refresh = serializers.CharField()  # Yangilanish uchun refresh token
