from rest_framework import serializers

from user_auth.models import Teacher, User, Departments, Course


# TeacherSerializer, o'qituvchi ma'lumotlarini serializatsiya qilish uchun ishlatiladi
class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = ["id", 'user', 'fullname', 'departments', 'course',
                  'descriptions']  # O'qituvchi haqida kerakli maydonlar


# TeacherUserSerializer, o'qituvchi foydalanuvchisining ma'lumotlarini serializatsiya qilish uchun
class TeacherUserSerializer(serializers.ModelSerializer):
    # Foydalanuvchi ma'lumotlarining ba'zi xususiyatlari faqat o'qish uchun
    is_active = serializers.BooleanField(read_only=True)
    is_teacher = serializers.BooleanField(read_only=True)
    is_admin = serializers.BooleanField(read_only=True)
    is_student = serializers.BooleanField(read_only=True)
    is_staff = serializers.BooleanField(read_only=True)

    class Meta:
        model = User  # Bu serializer User modelini ishlatadi
        fields = (
            'id', 'phone_number', 'password', 'email', 'is_active', 'is_teacher', 'is_staff', 'is_admin',
            'is_student')  # Foydalanuvchidan kerakli maydonlar


# TeacherPostSerializer, yangi o'qituvchi yaratish yoki yangilash uchun serializer
class TeacherPostSerializer(serializers.ModelSerializer):
    # Yangi o'qituvchi uchun kerakli maydonlar
    id = serializers.IntegerField(read_only=True)
    user = TeacherUserSerializer()  # O'qituvchining foydalanuvchi ma'lumotlarini alohida serializerda serializatsiya qilish
    fullname = serializers.CharField()  # To'liq ism
    departments = serializers.PrimaryKeyRelatedField(queryset=Departments.objects.all(), many=True)  # Departamentlar
    course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all(), many=True)  # Kurslar

    class Meta:
        model = Teacher  # O'qituvchi modelini ishlatadi
        fields = ["id", "user", "fullname", "departments", "course", "descriptions"]  # O'qituvchidan kerakli maydonlar

    def create(self, validated_data):
        # Yangi o'qituvchini yaratish
        user_db = validated_data.pop("user")  # Foydalanuvchi ma'lumotlarini ajratib olish
        user_db["is_active"] = True  # Foydalanuvchini faollashtirish
        user_db["is_teacher"] = True  # Foydalanuvchini o'qituvchi sifatida belgilash
        fullname = validated_data.pop("fullname")  # To'liq ismni olish
        departments_db = validated_data.pop("departments")  # Departamentlarni olish
        course_db = validated_data.pop("course")  # Kurslarni olish
        user = User.objects.create_user(**user_db)  # Yangi foydalanuvchini yaratish
        teacher = Teacher.objects.create(user=user, fullname=fullname, **validated_data)  # O'qituvchini yaratish
        teacher.departments.set(departments_db)  # Departamentlarni o'qituvchiga ulash
        teacher.course.set(course_db)  # Kurslarni o'qituvchiga ulash
        return teacher  # Yaratilgan o'qituvchini qaytarish

    def update(self, instance, validated_data):
        # Yangi ma'lumotlar bilan mavjud o'qituvchini yangilash
        user_data = validated_data.pop("user", None)  # Foydalanuvchi ma'lumotlarini olish
        departments = validated_data.pop("departments", None)  # Departamentlarni olish
        course = validated_data.pop("course", None)  # Kurslarni olish

        # USER UPDATE (Foydalanuvchini yangilash)
        user = instance.user  # Mavjud foydalanuvchi ma'lumotlari
        if user_data:
            user.phone_number = user_data.get("phone_number", user.phone_number)  # Telefon raqamini yangilash
            user.email = user_data.get("email", user.email)  # Email manzilini yangilash

            # Parolni yangilash
            password = user_data.get("password")
            if password:
                user.set_password(password)  # Yangi parolni o'rnatish

            user.save()  # Foydalanuvchini saqlash

        # TEACHER UPDATE (O'qituvchini yangilash)
        instance.fullname = validated_data.get("fullname", instance.fullname)  # To'liq ismini yangilash
        instance.descriptions = validated_data.get("descriptions", instance.descriptions)  # Tavsifni yangilash
        if departments is not None:
            instance.departments.set(departments)  # Departamentlarni yangilash
        if course is not None:
            instance.course.set(course)  # Kurslarni yangilash

        instance.save()  # O'qituvchini saqlash
        return instance  # Yangilangan o'qituvchini qaytarish


# DepartmentsSerializer, departamentlar uchun serializer
class DepartmentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Departments  # Departament modelini ishlatadi
        fields = '__all__'  # Barcha maydonlarni olish

