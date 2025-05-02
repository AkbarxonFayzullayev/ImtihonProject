from rest_framework import serializers

from user_auth.models import Student, User, Group, Parents


class StudentSerializer(serializers.ModelSerializer):
    is_line = serializers.BooleanField(read_only=True)

    class Meta:
        model = Student
        fields = ("id", 'user', 'group', 'is_line', 'descriptions')


class StudentUserSerializer(serializers.ModelSerializer):
    # is_line = serializers.BooleanField(read_only=True)
    is_active = serializers.BooleanField(read_only=True)
    is_teacher = serializers.BooleanField(read_only=True)
    is_admin = serializers.BooleanField(read_only=True)
    is_student = serializers.BooleanField(read_only=True)
    is_staff = serializers.BooleanField(read_only=True)

    class Meta:
        model = User
        fields = (
            'id', 'phone_number', 'password', 'email', 'is_active', 'is_teacher', 'is_staff', 'is_admin', 'is_student')

    def validate_is_student(self, value):
        return True


class StudentPostSerializer(serializers.Serializer):
    user = StudentUserSerializer()
    group = serializers.PrimaryKeyRelatedField(queryset=Group.objects.all(), many=True)

    class Meta:
        model = Student
        fields = ["id", "user", "group", "is_line", "descriptions"]
        read_only_fields = ["is_line"]

    def create(self, validated_data):
        user_db = validated_data.pop("user")
        group_db = validated_data.pop("group")
        user_db["is_active"] = True
        user_db["is_student"] = True
        user = User.objects.create_user(**user_db)
        student = Student.objects.create(user=user, **validated_data)
        student.group.set(group_db)
        return student


class ParentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parents
        fields = '__all__'
