from rest_framework import serializers

from user_auth.models import Student, User, Group, Parents


class StudentSerializer(serializers.ModelSerializer):
    is_line = serializers.BooleanField(read_only=True)

    class Meta:
        model = Student
        fields = ("id", 'user','fullname', 'group', 'is_line', 'descriptions')


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
    fullname = serializers.CharField()
    group = serializers.PrimaryKeyRelatedField(queryset=Group.objects.all(), many=True)

    class Meta:
        model = Student
        fields = ["id","user","fullname", "group", "is_line", "descriptions"]
        read_only_fields = ["is_line"]

    def create(self, validated_data):
        user_db = validated_data.pop("user")
        fullname = validated_data.pop("fullname")
        group_db = validated_data.pop("group")
        user_db["is_active"] = True
        user_db["is_student"] = True
        user = User.objects.create_user(**user_db)
        student = Student.objects.create(user=user,fullname=fullname, **validated_data)
        student.group.set(group_db)
        return student

    def update(self, instance, validated_data):
        user_data = validated_data.pop("user", None)
        group = validated_data.pop("group", None)

        # USER UPDATE
        user = instance.user
        if user_data:
            user.phone_number = user_data.get("phone_number", user.phone_number)
            user.email = user_data.get("email", user.email)

            password = user_data.get("password")
            if password:
                user.set_password(password)

            user.save()

        # Student UPDATE
        instance.fullname = validated_data.get("fullname", instance.fullname)
        instance.descriptions = validated_data.get("descriptions", instance.descriptions)
        if group is not None:
            instance.group.set(group)

        instance.save()
        return instance


class ParentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parents
        fields = '__all__'
