from rest_framework import serializers

from user_auth.models import Teacher


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ["id", 'user', 'departments', 'course', 'descriptions']

