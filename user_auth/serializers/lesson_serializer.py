from rest_framework import serializers

from ..models import Lesson, Group, Student, LessonAttendance, Table
from .homework_serializer import GroupHomeWorkSerializer


class LessonSerializer(serializers.ModelSerializer):
    group = serializers.PrimaryKeyRelatedField(queryset=Group.objects.all())
    homework = GroupHomeWorkSerializer(many=True, read_only=True)

    class Meta:
        model = Lesson
        fields = ['id', 'title', 'group', 'date', 'table', 'descriptions', 'homework']
        ref_name = 'HomeWorkSerializer'


class LessonAttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonAttendance
        fields = ['id', 'lesson', 'student', 'status']


class LessonCreateSerializer(serializers.Serializer):
    group = serializers.IntegerField()
    title = serializers.CharField()
    date = serializers.DateField()
    table = serializers.IntegerField()
    descriptions = serializers.CharField(required=False)
    kelgan_studentlar = serializers.ListField(child=serializers.IntegerField(), required=True)
    sababli_studentlar = serializers.ListField(child=serializers.IntegerField(), required=True)

    def validate_group(self, value):
        if not Group.objects.filter(id=value).exists():
            raise serializers.ValidationError("Bunday group mavjud emas.")

        return value

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

    def create(self, validated_data):
        table_id = validated_data.pop('table')
        table = Table.objects.get(id=table_id)
        group_id = validated_data.pop('group')
        kelgan_ids = validated_data.pop('kelgan_studentlar', [])
        sababli_ids = validated_data.pop('sababli_studentlar', [])

        group = Group.objects.get(id=group_id)
        lesson = Lesson.objects.create(group=group,table=table, **validated_data)

        all_students = group.students.all()
        hadir_student_ids = set(kelgan_ids + sababli_ids)
        all_student_ids = set(all_students.values_list('id', flat=True))
        kelmagan_ids = all_student_ids - hadir_student_ids

        # LessonAttendance larni tayyorlash
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

        LessonAttendance.objects.bulk_create(lesson_attendances)

        return lesson


class LessonUpdateSerializer(serializers.Serializer):
    group = serializers.IntegerField(required=False)
    title = serializers.CharField(required=False)
    date = serializers.DateField(required=False)
    table = serializers.IntegerField(required=False)
    descriptions = serializers.CharField(required=False)
    kelgan_studentlar = serializers.ListField(child=serializers.IntegerField(), required=False)
    sababli_studentlar = serializers.ListField(child=serializers.IntegerField(), required=False)

    def validate_group(self, value):
        if not Group.objects.filter(id=value).exists():
            raise serializers.ValidationError("Bunday group mavjud emas.")
        return value

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

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.date = validated_data.get('date', instance.date)

        # 'table' maydonini yangilash
        table_id = validated_data.get('table', None)
        if table_id:
            try:
                instance.table = Table.objects.get(id=table_id)  # Table instansiyasini olish
            except Table.DoesNotExist:
                raise serializers.ValidationError("Bunday table mavjud emas.")

        instance.descriptions = validated_data.get('descriptions', instance.descriptions)
        instance.save()

        kelgan_ids = validated_data.get('kelgan_studentlar', [])
        sababli_ids = validated_data.get('sababli_studentlar', [])

        # Oldin barcha davomatlarni yangilash
        for student_id in kelgan_ids + sababli_ids:
            lesson_attendance = LessonAttendance.objects.get(lesson=instance, student_id=student_id)
            if student_id in kelgan_ids:
                lesson_attendance.status = 'keldi'
            else:
                lesson_attendance.status = 'sababli'
            lesson_attendance.save()

        # Kelmaganlarni yangilash
        all_students = Student.objects.filter(group=instance.group)
        attended_student_ids = set(kelgan_ids + sababli_ids)
        for student in all_students:
            if student.id not in attended_student_ids:
                lesson_attendance = LessonAttendance.objects.get(lesson=instance, student_id=student.id)
                lesson_attendance.status = 'kelmadi'
                lesson_attendance.save()

        return instance
