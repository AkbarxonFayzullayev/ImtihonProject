from rest_framework import serializers
#
from user_auth.models import Teacher, User, Departments, Course
# from ..serializers import *
from user_auth.serializers.login_serializers import UserSerializer



class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ["id", 'user', 'departments', 'course', 'descriptions']


class TeacherUserSerializer(serializers.ModelSerializer):
    is_active = serializers.BooleanField(read_only=True)
    is_teacher = serializers.BooleanField(read_only=True)
    is_admin = serializers.BooleanField(read_only=True)
    is_student = serializers.BooleanField(read_only=True)
    is_staff = serializers.BooleanField(read_only=True)
    class Meta:
        model = User
        fields = ('id','phone_number','password','email','is_active','is_teacher','is_staff','is_admin','is_student')

    # def validate_is_teacher(self, value):
    #     return True



class TeacherPostSerializer(serializers.Serializer):
    user = TeacherUserSerializer()
    departments = serializers.PrimaryKeyRelatedField(queryset=Departments.objects.all(),many=True)
    course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all(),many=True)
    class Meta:
        model = Teacher
        fields = ["id","user","departments","course","descriptions"]

    def create(self, validated_data):
        user_db = validated_data.pop("user")
        user_db["is_active"] = True
        user_db["is_teacher"] = True
        departments_db = validated_data.pop("departments")
        course_db = validated_data.pop("course")
        user = User.objects.create_user(**user_db)
        teacher = Teacher.objects.create(user=user,**validated_data)
        teacher.departments.set(departments_db)
        teacher.course.set(course_db)
        return teacher
