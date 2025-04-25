from rest_framework import serializers
from user_auth.models import Attendance, StudentAttendance, Student, Group, Teacher
from user_auth.models.model_attendance import TeacherAttendance

class StudentAttendanceSerializer(serializers.ModelSerializer):
    student = serializers.PrimaryKeyRelatedField(queryset=Student.objects.all())
    date = serializers.DateField(source='attendance.date', read_only=True)
    class Meta:
        model = StudentAttendance
        fields = ['student', 'status','date']

class AttendanceCreateSerializer(serializers.Serializer):
    group = serializers.PrimaryKeyRelatedField(queryset=Group.objects.all())
    date = serializers.DateField()
    descriptions = serializers.CharField(required=False, allow_blank=True)
    attendances = serializers.DictField(
        child=serializers.ChoiceField(choices=["bor", "yo'q", "kechikkan","sababli"])
    )

    def validate(self, data):
        group = data['group']
        group_student_ids = set(group.students.values_list('id', flat=True))
        provided_ids = set(map(int, data['attendances'].keys()))

        # Tekshirish: barcha attendances idlari guruhga tegishli bo'lishi kerak
        if not provided_ids.issubset(group_student_ids):
            raise serializers.ValidationError("Ba'zi student IDlar ushbu guruhga tegishli emas.")
        return data

    def create(self, validated_data):
        group = validated_data['group']
        date = validated_data['date']
        descriptions = validated_data.get('descriptions', '')
        attendance = Attendance.objects.create(group=group, date=date, descriptions=descriptions)

        student_attendances = []
        for student_id_str, status in validated_data['attendances'].items():
            student_id = int(student_id_str)
            student = Student.objects.get(pk=student_id)
            student_attendances.append(
                StudentAttendance(attendance=attendance, student=student, status=status)
            )

        StudentAttendance.objects.bulk_create(student_attendances)
        return attendance

    def update(self, instance, validated_data):
        # Update attendance description
        instance.descriptions = validated_data.get('descriptions', instance.descriptions)
        instance.save()

        # Update student attendance statuses
        for student_id_str, status in validated_data['attendances'].items():
            student_id = int(student_id_str)
            student_attendance = StudentAttendance.objects.filter(
                attendance=instance, student_id=student_id
            ).first()

            if student_attendance:
                student_attendance.status = status
                student_attendance.save()

        return instance

class TeacherAttendanceSerializer(serializers.ModelSerializer):
    teacher = serializers.PrimaryKeyRelatedField(queryset=Teacher.objects.all())
    class Meta:
        model = TeacherAttendance
        fields = ["teacher","status"]

class TeacherAttendanceCreateSerializer(serializers.Serializer):
    group = serializers.PrimaryKeyRelatedField(queryset=Group.objects.all())
    date = serializers.DateField()
    descriptions = serializers.CharField(required=False, allow_blank=True)
    attendances = serializers.DictField(
        child=serializers.ChoiceField(choices=["bor", "yo'q", "kechikkan", "sababli"])
    )

    def create(self, validated_data):
        group = validated_data["group"]
        date = validated_data["date"]
        descriptions = validated_data.get('descriptions', '')
        attendance = Attendance.objects.create(group=group,date=date,descriptions=descriptions)

        teacher_attendances = []
        for teacher_id_str, status in validated_data['attendances'].items():
            teacher_id = int(teacher_id_str)
            teacher = Teacher.objects.get(pk=teacher_id)
            teacher_attendances.append(
                TeacherAttendance(attendance=attendance, teacher=teacher, status=status)
            )

        TeacherAttendance.objects.bulk_create(teacher_attendances)
        return attendance



class StudentAttendancesSerializer(serializers.ModelSerializer):
    student_id = serializers.IntegerField(source='student.id')
    student_name = serializers.CharField(source='student.full_name')  # yoki first_name, last_name

    class Meta:
        model = StudentAttendance
        fields = ['student_id', 'student_name', 'status']

class AttendanceListSerializer(serializers.ModelSerializer):
    attendances = StudentAttendanceSerializer(source='student_attendances', many=True)
    group_id = serializers.IntegerField(source='group.id')
    group_title = serializers.CharField(source='group.title')  # yoki `name`, `title`... modelga qarab

    class Meta:
        model = Attendance
        fields = ['id', 'group_id', 'group_title', 'date', 'descriptions', 'attendances']

