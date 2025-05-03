from django.contrib.auth import authenticate
from rest_framework import serializers

from ..models import *


class LoginSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        phone_number = attrs.get("phone_number")
        password = attrs.get("password")
        try:
            user = User.objects.get(phone_number=phone_number)
        except User.DoesNotExist:
            raise serializers.ValidationError({"success": False, "detail": "User topilmadi"})

        auth_user = authenticate(phone_number=user.phone_number, password=password)
        if auth_user is None:
            raise serializers.ValidationError({"success": False, "detail": "phone_number yoki password xato"})
        attrs["user"] = auth_user
        return attrs


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'phone_number', 'password', 'is_active', 'is_staff', "is_teacher", 'is_admin', 'is_student')


class StaffUserSerializer(serializers.ModelSerializer):
    is_active = serializers.BooleanField(read_only=True)
    is_staff = serializers.BooleanField(read_only=True)
    is_teacher = serializers.BooleanField(read_only=True)
    is_admin = serializers.BooleanField(read_only=True)
    is_student = serializers.BooleanField(read_only=True)

    class Meta:
        model = User
        fields = ('id', 'phone_number', 'password', 'is_active', 'is_staff', "is_teacher", 'is_admin', 'is_student')

    def create(self, validated_data):
        validated_data['is_active'] = True
        validated_data['is_staff'] = True
        user = User.objects.create_user(**validated_data)
        return user


class ChangePasswordSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True)
    re_new_password = serializers.CharField(required=True, write_only=True)

    def update(self, instance, validated_data):
        instance.password = validated_data.get('password', instance.password)

        if not validated_data['new_password']:
            raise serializers.ValidationError({'new_password': 'new_password kiritilishi shart'})

        if not validated_data['old_password']:
            raise serializers.ValidationError({'old_password': 'old_password kiritilishi shart'})

        if not instance.check_password(validated_data['old_password']):
            raise serializers.ValidationError({'old_password': 'old_password xato'})

        if validated_data['new_password'] != validated_data['re_new_password']:
            raise serializers.ValidationError({'passwords': "new_password va renew_password bir biriga teng bo'lishi kerak"})

        if validated_data['new_password'] == validated_data['re_new_password'] and instance.check_password(
                validated_data['old_password']):
            instance.set_password(validated_data['new_password'])
            instance.save()
            return instance

    class Meta:
        model = User
        fields = ['old_password', 'new_password', 're_new_password']


class SetPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, data):
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError("Parollar mos emas.")
        return data


class SMSSerializer(serializers.Serializer):
    phone_number = serializers.CharField()


class VerifySMSSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    verification_code = serializers.CharField()
    new_password = serializers.CharField()
    renew_password = serializers.CharField()

class RefreshTokenSerializer(serializers.Serializer):
    refresh = serializers.CharField()