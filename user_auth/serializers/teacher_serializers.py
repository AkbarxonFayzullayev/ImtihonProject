from rest_framework import serializers
#
from user_auth.models import Teacher
# from ..serializers import *
from user_auth.serializers.login_serializers import UserSerializer



class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ["id", 'user', 'departments', 'course', 'descriptions']

class TeacherPostSerializer(serializers.Serializer):
    user = UserSerializer()
    teacher = TeacherSerializer()
