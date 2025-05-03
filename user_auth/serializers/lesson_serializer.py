from rest_framework import serializers

from ..models import Lesson, Group, Student, LessonAttendance, Table
from .homework_serializer import GroupHomeWorkSerializer


# LessonSerializer, dars ma'lumotlarini serializatsiya qilish uchun ishlatiladi
class LessonSerializer(serializers.ModelSerializer):
    group = serializers.PrimaryKeyRelatedField(queryset=Group.objects.all())  # Guruhni tanlash
    homework = GroupHomeWorkSerializer(many=True, read_only=True)  # Uy vazifalari bilan bog'lanish

    class Meta:
        model = Lesson  # Dars modelini ishlatadi
        fields = ['id', 'title', 'group', 'date', 'table', 'descriptions', 'homework']  # Darsning kerakli maydonlari
        ref_name = 'HomeWorkSerializer'  # Bu serializer nomini belgilash


# LessonAttendanceSerializer, darsga qatnashish holatini serializatsiya qilish uchun
class LessonAttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonAttendance  # Davomat modelini ishlatadi
        fields = ['id', 'lesson', 'student', 'status']  # Dars, talaba va qatnashish holati


# LessonCreateSerializer, yangi dars yaratish uchun serializer
class LessonCreateSerializer(serializers.Serializer):
    group = serializers.IntegerField()  # Guruh ID
    title = serializers.CharField()  # Dars nomi
    date = serializers.DateField()  # Dars sanasi
    table = serializers.IntegerField()  # Jadval ID
    descriptions = serializers.CharField(required=False)  # Dars tavsifi (ixtiyoriy)
    kelgan_studentlar = serializers.ListField(child=serializers.IntegerField(), required=True)  # Kelgan talabalar
    sababli_studentlar = serializers.ListField(child=serializers.IntegerField(), required=True)  # Sababli talabalar

    # Guruhni tekshirish
    def validate_group(self, value):
        if not Group.objects.filter(id=value).exists():  # Guruh mavjudligini tekshirish
            raise serializers.ValidationError("Bunday group mavjud emas.")
        return value

    # Umumiy validatsiya
    def validate(self, attrs):
        kelgan = attrs.get('kelgan_studentlar', [])
        sababli = attrs.get('sababli_studentlar', [])
        all_ids = kelgan + sababli

        if not all_ids:  # Hech qanday talaba yuborilmasa, xato
            raise serializers.ValidationError("Hech qanday student yuborilmadi.")

        group_id = attrs['group']
        students = Student.objects.filter(id__in=all_ids, group=group_id)  # Talabalar guruhiga qarab filtrlash

        if students.count() != len(set(all_ids)):  # Agar studentlar noto'g'ri ID yoki boshqa guruhdan bo'lsa
            raise serializers.ValidationError("Student IDlar noto'g'ri yoki boshqa guruhdan.")
        return attrs

    # Yangi darsni yaratish
    def create(self, validated_data):
        table_id = validated_data.pop('table')  # Jadval ID olish
        table = Table.objects.get(id=table_id)  # Jadvalni olish
        group_id = validated_data.pop('group')  # Guruh ID olish
        kelgan_ids = validated_data.pop('kelgan_studentlar', [])  # Kelgan talabalar IDlarini olish
        sababli_ids = validated_data.pop('sababli_studentlar', [])  # Sababli talabalar IDlarini olish

        group = Group.objects.get(id=group_id)  # Guruhni olish
        lesson = Lesson.objects.create(group=group, table=table, **validated_data)  # Yangi darsni yaratish

        # Guruhdagi barcha talabalarni olish
        all_students = group.students.all()
        hadir_student_ids = set(kelgan_ids + sababli_ids)  # Kelgan va sababli talabalar IDlarini olish
        all_student_ids = set(all_students.values_list('id', flat=True))  # Barcha talabalar IDlarini olish
        kelmagan_ids = all_student_ids - hadir_student_ids  # Kelmagan talabalar

        # Davomatlarni yaratish
        lesson_attendances = []

        # Kelganlar
        for student_id in kelgan_ids:
            lesson_attendances.append(LessonAttendance(
                lesson=lesson,
                student_id=student_id,
                status='keldi'
            ))

        # Sabablilar
        for student_id in sababli_ids:
            lesson_attendances.append(LessonAttendance(
                lesson=lesson,
                student_id=student_id,
                status='sababli'
            ))

        # Kelmaganlar
        for student_id in kelmagan_ids:
            lesson_attendances.append(LessonAttendance(
                lesson=lesson,
                student_id=student_id,
                status='kelmadi'
            ))

        LessonAttendance.objects.bulk_create(lesson_attendances)  # Davomatlarni ma'lumotlar bazasiga saqlash

        return lesson  # Yaratilgan darsni qaytarish


# LessonUpdateSerializer, mavjud darsni yangilash uchun serializer
class LessonUpdateSerializer(serializers.Serializer):
    group = serializers.IntegerField(required=False)  # Guruh ID (ixtiyoriy)
    title = serializers.CharField(required=False)  # Dars nomi (ixtiyoriy)
    date = serializers.DateField(required=False)  # Dars sanasi (ixtiyoriy)
    table = serializers.IntegerField(required=False)  # Jadval ID (ixtiyoriy)
    descriptions = serializers.CharField(required=False)  # Tavsif (ixtiyoriy)
    kelgan_studentlar = serializers.ListField(child=serializers.IntegerField(),
                                              required=False)  # Kelgan talabalar (ixtiyoriy)
    sababli_studentlar = serializers.ListField(child=serializers.IntegerField(),
                                               required=False)  # Sababli talabalar (ixtiyoriy)

    # Guruhni tekshirish
    def validate_group(self, value):
        if not Group.objects.filter(id=value).exists():
            raise serializers.ValidationError("Bunday group mavjud emas.")
        return value

    # Umumiy validatsiya
    def validate(self, attrs):
        kelgan = attrs.get('kelgan_studentlar', [])
        sababli = attrs.get('sababli_studentlar', [])
        all_ids = kelgan + sababli

        if not all_ids:
            raise serializers.ValidationError("Hech qanday student yuborilmadi.")

        group_id = attrs['group']
        students = Student.objects.filter(id__in=all_ids, group=group_id)

        if students.count() != len(set(all_ids)):
            raise serializers.ValidationError("Student IDlar noto'g'ri yoki boshqa guruhdan.")
        return attrs

    # Mavjud darsni yangilash
    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)  # Dars nomini yangilash
        instance.date = validated_data.get('date', instance.date)  # Dars sanasini yangilash

        # Jadvalni yangilash
        table_id = validated_data.get('table', None)
        if table_id:
            try:
                instance.table = Table.objects.get(id=table_id)  # Jadvalni olish
            except Table.DoesNotExist:
                raise serializers.ValidationError("Bunday table mavjud emas.")

        instance.descriptions = validated_data.get('descriptions', instance.descriptions)  # Tavsifni yangilash
        instance.save()

        kelgan_ids = validated_data.get('kelgan_studentlar', [])
        sababli_ids = validated_data.get('sababli_studentlar', [])

        # Avvalgi davomatlarni yangilash
        for student_id in kelgan_ids + sababli_ids:
            lesson_attendance = LessonAttendance.objects.get(lesson=instance, student_id=student_id)
            if student_id in kelgan_ids:
                lesson_attendance.status = 'keldi'  # Kelgan talaba
            else:
                lesson_attendance.status = 'sababli'  # Sababli talaba
            lesson_attendance.save()

        # Kelmaganlarni yangilash
        all_students = Student.objects.filter(group=instance.group)
        attended_student_ids = set(kelgan_ids + sababli_ids)
        for student in all_students:
            if student.id not in attended_student_ids:
                lesson_attendance = LessonAttendance.objects.get(lesson=instance, student_id=student.id)
                lesson_attendance.status = 'kelmadi'  # Kelmagan talaba
                lesson_attendance.save()

        return instance  # Yangilangan darsni qaytarish
