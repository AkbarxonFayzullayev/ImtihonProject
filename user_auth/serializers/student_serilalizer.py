from rest_framework import serializers

from user_auth.models import Student, User, Group, Parents


# StudentSerializer - Student modelini serializatsiya qilish
class StudentSerializer(serializers.ModelSerializer):
    is_line = serializers.BooleanField(read_only=True)  # Foydalanuvchining "line" holatini faqat o'qish

    class Meta:
        model = Student  # Student modeli
        fields = ("id", 'user', 'fullname', 'group', 'is_line', 'descriptions')  # Kerakli maydonlar


# StudentUserSerializer - User modelini Student bilan bog'langan holda serializatsiya qilish
class StudentUserSerializer(serializers.ModelSerializer):
    is_active = serializers.BooleanField(read_only=True)  # Foydalanuvchining faoliyat holatini faqat o'qish
    is_teacher = serializers.BooleanField(read_only=True)  # O'qituvchi holatini faqat o'qish
    is_admin = serializers.BooleanField(read_only=True)  # Admin holatini faqat o'qish
    is_student = serializers.BooleanField(read_only=True)  # Talaba holatini faqat o'qish
    is_staff = serializers.BooleanField(read_only=True)  # Xodim holatini faqat o'qish

    class Meta:
        model = User  # User modeli
        fields = (
            'id', 'phone_number', 'password', 'email', 'is_active', 'is_teacher', 'is_staff', 'is_admin',
            'is_student')  # Kerakli maydonlar

    def validate_is_student(self, value):
        return True  # 'is_student' maydoni doim True bo'ladi


# StudentPostSerializer - Yangi Student yaratish yoki mavjud Studentni yangilash uchun serializer
class StudentPostSerializer(serializers.Serializer):
    user = StudentUserSerializer()  # Foydalanuvchi (User) haqida ma'lumot
    fullname = serializers.CharField()  # Foydalanuvchining to'liq ismi
    group = serializers.PrimaryKeyRelatedField(queryset=Group.objects.all(), many=True)  # Foydalanuvchining guruhlari

    class Meta:
        model = Student  # Student modeli
        fields = ["id", "user", "fullname", "group", "is_line", "descriptions"]  # Kerakli maydonlar
        read_only_fields = ["is_line"]  # 'is_line' faqat o'qish

    def create(self, validated_data):
        user_db = validated_data.pop("user")  # User ma'lumotlarini olib tashlash
        fullname = validated_data.pop("fullname")  # To'liq ismni olib tashlash
        group_db = validated_data.pop("group")  # Guruhlarni olib tashlash
        user_db["is_active"] = True  # Yangi foydalanuvchi faol bo'lishi kerak
        user_db["is_student"] = True  # Foydalanuvchi talaba sifatida belgilanishi kerak
        user = User.objects.create_user(**user_db)  # Yangi foydalanuvchini yaratish
        student = Student.objects.create(user=user, fullname=fullname, **validated_data)  # Yangi talaba yaratish
        student.group.set(group_db)  # Guruhlarni o'rnatish
        return student

    def update(self, instance, validated_data):
        user_data = validated_data.pop("user", None)  # Foydalanuvchi ma'lumotlarini olish
        group = validated_data.pop("group", None)  # Guruhlarni olish

        # Foydalanuvchini yangilash
        user = instance.user
        if user_data:
            user.phone_number = user_data.get("phone_number", user.phone_number)  # Telefon raqamini yangilash
            user.email = user_data.get("email", user.email)  # Emailni yangilash

            password = user_data.get("password")  # Parolni tekshirish
            if password:
                user.set_password(password)  # Parolni yangilash

            user.save()  # Foydalanuvchining o'zgarishlarini saqlash

        # Talabani yangilash
        instance.fullname = validated_data.get("fullname", instance.fullname)  # To'liq ismini yangilash
        instance.descriptions = validated_data.get("descriptions", instance.descriptions)  # Tasvirni yangilash
        if group is not None:
            instance.group.set(group)  # Guruhlarni yangilash

        instance.save()  # Talabani saqlash
        return instance


# ParentsSerializer - Parents modelini serializatsiya qilish
class ParentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parents  # Parents modeli
        fields = '__all__'  # Barcha maydonlarni olish
