from rest_framework import serializers
from user_auth.models import  Student, Group, Teacher, LessonAttendance, HomeWork, Lesson, GroupHomeWork


# from user_auth.models.model_attendance import TeacherAttendance

# class StudentAttendanceSerializer(serializers.ModelSerializer):
#     student = serializers.PrimaryKeyRelatedField(queryset=Student.objects.all())
#     date = serializers.DateField(source='attendance.date', read_only=True)
#     class Meta:
#         model = StudentAttendance
#         fields = ['student', 'status','date']
#
# class AttendanceCreateSerializer(serializers.Serializer):
#     group = serializers.PrimaryKeyRelatedField(queryset=Group.objects.all())
#     date = serializers.DateField()
#     descriptions = serializers.CharField(required=False, allow_blank=True)
#     attendances = serializers.DictField(
#         child=serializers.ChoiceField(choices=["bor", "yo'q", "kechikkan","sababli"])
#     )
#
#     def validate(self, data):
#         group = data['group']
#         group_student_ids = set(group.students.values_list('id', flat=True))
#         provided_ids = set(map(int, data['attendances'].keys()))
#
#         # Tekshirish: barcha attendances idlari guruhga tegishli bo'lishi kerak
#         if not provided_ids.issubset(group_student_ids):
#             raise serializers.ValidationError("Ba'zi student IDlar ushbu guruhga tegishli emas.")
#         return data
#
#     def create(self, validated_data):
#         group = validated_data['group']
#         date = validated_data['date']
#         descriptions = validated_data.get('descriptions', '')
#         attendance = Attendance.objects.create(group=group, date=date, descriptions=descriptions)
#
#         student_attendances = []
#         for student_id_str, status in validated_data['attendances'].items():
#             student_id = int(student_id_str)
#             student = Student.objects.get(pk=student_id)
#             student_attendances.append(
#                 StudentAttendance(attendance=attendance, student=student, status=status)
#             )
#
#         StudentAttendance.objects.bulk_create(student_attendances)
#         return attendance
#
#     def update(self, instance, validated_data):
#         # Update attendance description
#         instance.descriptions = validated_data.get('descriptions', instance.descriptions)
#         instance.save()
#
#         # Update student attendance statuses
#         for student_id_str, status in validated_data['attendances'].items():
#             student_id = int(student_id_str)
#             student_attendance = StudentAttendance.objects.filter(
#                 attendance=instance, student_id=student_id
#             ).first()
#
#             if student_attendance:
#                 student_attendance.status = status
#                 student_attendance.save()
#
#         return instance
#
# class TeacherAttendanceSerializer(serializers.ModelSerializer):
#     teacher = serializers.PrimaryKeyRelatedField(queryset=Teacher.objects.all())
#     class Meta:
#         model = TeacherAttendance
#         fields = ["teacher","status"]
#
# class TeacherAttendanceCreateSerializer(serializers.Serializer):
#     group = serializers.PrimaryKeyRelatedField(queryset=Group.objects.all())
#     date = serializers.DateField()
#     descriptions = serializers.CharField(required=False, allow_blank=True)
#     attendances = serializers.DictField(
#         child=serializers.ChoiceField(choices=["bor", "yo'q", "kechikkan", "sababli"])
#     )
#
#     def create(self, validated_data):
#         group = validated_data["group"]
#         date = validated_data["date"]
#         descriptions = validated_data.get('descriptions', '')
#         attendance = Attendance.objects.create(group=group,date=date,descriptions=descriptions)
#
#         teacher_attendances = []
#         for teacher_id_str, status in validated_data['attendances'].items():
#             teacher_id = int(teacher_id_str)
#             teacher = Teacher.objects.get(pk=teacher_id)
#             teacher_attendances.append(
#                 TeacherAttendance(attendance=attendance, teacher=teacher, status=status)
#             )
#
#         TeacherAttendance.objects.bulk_create(teacher_attendances)
#         return attendance
#
#
#
# class StudentAttendancesSerializer(serializers.ModelSerializer):
#     student_id = serializers.IntegerField(source='student.id')
#     student_name = serializers.CharField(source='student.full_name')  # yoki first_name, last_name
#
#     class Meta:
#         model = StudentAttendance
#         fields = ['student_id', 'student_name', 'status']
#
# class AttendanceListSerializer(serializers.ModelSerializer):
#     attendances = StudentAttendanceSerializer(source='student_attendances', many=True)
#     group_id = serializers.IntegerField(source='group.id')
#     group_title = serializers.CharField(source='group.title')  # yoki `name`, `title`... modelga qarab
#
#     class Meta:
#         model = Attendance
#         fields = ['id', 'group_id', 'group_title', 'date', 'descriptions', 'attendances']
#
#
# class AttendanceCreateSerializer(serializers.Serializer):
#     group = serializers.IntegerField()
#     date = serializers.DateField()
#     kelgan_studentlar = serializers.ListField(child=serializers.IntegerField(), required=False)
#     # kelmagan_studentlar = serializers.ListField(child=serializers.IntegerField(), required=False)
#     sababli_studentlar = serializers.ListField(child=serializers.IntegerField(), required=False)
#
#     def validate_group_id(self, value):
#         if not Group.objects.filter(id=value).exists():
#             raise serializers.ValidationError("Bunday group mavjud emas.")
#         return value
#
#     def validate(self, attrs):
#         # Student ID larni tekshirish
#         all_ids = (attrs.get('kelgan_studentlar', []) +
#                    attrs.get('kelmagan_studentlar', []) +
#                    attrs.get('sababli_studentlar', []))
#         if not all_ids:
#             raise serializers.ValidationError("Hech qanday student yuborilmadi.")
#
#         students = Student.objects.filter(id__in=all_ids, group=attrs['group'])
#         if students.count() != len(set(all_ids)):
#             raise serializers.ValidationError("Student IDlar noto'g'ri yoki boshqa groupdan.")
#         return attrs
#
#     def create(self, validated_data):
#         group_id = validated_data['group']
#         group = Group.objects.get(id=group_id)
#         date = validated_data['date']
#         kelgan = validated_data.get('kelgan_studentlar', [])
#         sababli = validated_data.get('sababli_studentlar', [])
#
#         attendances = []
#
#         # Barcha student id larini olish
#         all_students = group.students.all()
#         all_students_dict = {student.id: student for student in all_students}
#
#         all_student_ids = set(all_students_dict.keys())
#         hadir_student_ids = set(kelgan + sababli)
#         kelmagan_ids = all_student_ids - hadir_student_ids
#
#         # Kelganlar uchun
#         for student_id in kelgan:
#             student = all_students_dict.get(student_id)
#             if student:
#                 attendances.append(Attendance(
#                     group=group,
#                     student=student,
#                     date=date,
#                     status='keldi'
#                 ))
#
#         # Sababli uchun
#         for student_id in sababli:
#             student = all_students_dict.get(student_id)
#             if student:
#                 attendances.append(Attendance(
#                     group=group,
#                     student=student,
#                     date=date,
#                     status='sababli'
#                 ))
#
#         # Kelmaganlar uchun
#         for student_id in kelmagan_ids:
#             student = all_students_dict.get(student_id)
#             if student:
#                 attendances.append(Attendance(
#                     group=group,
#                     student=student,
#                     date=date,
#                     status='kelmadi'
#                 ))
#
#         # Bulk create
#         Attendance.objects.bulk_create(attendances)
#
#         return attendances

class LessonAttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonAttendance
        fields = ['id', 'lesson', 'student', 'status']

class HomeWorkSerializer(serializers.ModelSerializer):
    class Meta:
        model = HomeWork
        fields = ['id', 'groupHomeWork', 'score', 'student', 'link', 'is_active', 'descriptions']

class GroupHomeWorkSerializer(serializers.ModelSerializer):
    lesson = serializers.PrimaryKeyRelatedField(queryset=Lesson.objects.all())
    class Meta:
        model = GroupHomeWork
        fields = ['id', 'group', 'lesson', 'file', 'is_active', 'descriptions']
        ref_name = 'GroupHomeWorkSerializer'

class LessonSerializer(serializers.ModelSerializer):
    group = serializers.PrimaryKeyRelatedField(queryset=Group.objects.all())
    homework = GroupHomeWorkSerializer(many=True, read_only=True)

    class Meta:
        model = Lesson
        fields = ['id', 'title', 'group', 'date', 'start_time', 'end_time', 'descriptions', 'homework']
        ref_name = 'HomeWorkSerializer'


# class LessonCreateSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Lesson
#         fields = ['id', 'title', 'group', 'date', 'start_time', 'end_time', 'descriptions']

class LessonCreateSerializer(serializers.Serializer):
    group = serializers.IntegerField()
    title = serializers.CharField()
    date = serializers.DateField()
    start_time = serializers.TimeField()
    end_time = serializers.TimeField()
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
        group_id = validated_data.pop('group')
        kelgan_ids = validated_data.pop('kelgan_studentlar', [])
        sababli_ids = validated_data.pop('sababli_studentlar', [])

        group = Group.objects.get(id=group_id)
        lesson = Lesson.objects.create(group=group, **validated_data)

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

#
# class LessonAttendanceCreateSerializer(serializers.Serializer):
#     group = serializers.IntegerField()
#     date = serializers.DateField()
#     kelgan_studentlar = serializers.ListField(child=serializers.IntegerField(), required=True)
#     sababli_studentlar = serializers.ListField(child=serializers.IntegerField(), required=True)
#
#     def validate(self, attrs):
#         group_id = attrs.get('group')
#         kelgan = attrs.get('kelgan_studentlar', [])
#         sababli = attrs.get('sababli_studentlar', [])
#
#         # Guruhni tekshirish
#         group = Group.objects.filter(id=group_id).first()
#         if not group:
#             raise serializers.ValidationError("Bunday guruh mavjud emas.")
#
#         # Studentlarni tekshirish
#         all_students = Student.objects.filter(id__in=kelgan + sababli, group=group_id)
#         if all_students.count() != len(set(kelgan + sababli)):
#             raise serializers.ValidationError("Student IDlar noto'g'ri yoki boshqa guruhdan.")
#
#         # Kelmaganlarni hisoblash
#         all_student_ids = set(Student.objects.filter(group=group_id).values_list('id', flat=True))
#         hadir_student_ids = set(kelgan + sababli)
#         kelmagan_ids = all_student_ids - hadir_student_ids
#
#         return {
#             'group': group_id,
#             'date': attrs['date'],
#             'kelgan_studentlar': kelgan,
#             'sababli_studentlar': sababli,
#             'kelmagan_studentlar': list(kelmagan_ids),
#         }
#
#     def create(self, validated_data):
#         group_id = validated_data['group']
#         group = Group.objects.get(id=group_id)
#         date = validated_data['date']
#         kelgan = validated_data.get('kelgan_studentlar', [])
#         sababli = validated_data.get('sababli_studentlar', [])
#         kelmagan = validated_data.get('kelmagan_studentlar', [])
#
#         # Lesson yaratish
#         lesson = Lesson.objects.create(group=group, date=date)
#
#         # LessonAttendance yaratish
#         attendances = []
#         all_students = Student.objects.filter(id__in=kelgan + sababli + kelmagan, group=group)
#
#         # Kelganlar uchun
#         for student_id in kelgan:
#             student = all_students.get(id=student_id)
#             attendances.append(LessonAttendance(
#                 lesson=lesson,
#                 student=student,
#                 date=date,
#                 status='keldi'
#             ))
#
#         # Sababli studentlar uchun
#         for student_id in sababli:
#             student = all_students.get(id=student_id)
#             attendances.append(LessonAttendance(
#                 lesson=lesson,
#                 student=student,
#                 date=date,
#                 status='sababli'
#             ))
#
#         # Kelmaganlar uchun
#         for student_id in kelmagan:
#             student = all_students.get(id=student_id)
#             attendances.append(LessonAttendance(
#                 lesson=lesson,
#                 student=student,
#                 date=date,
#                 status='kelmadi'
#             ))
#
#         # Bulk create qilish
#         LessonAttendance.objects.bulk_create(attendances)
#
#         return attendances
