from rest_framework import serializers
from user_auth.models import Attendance, StudentAttendance, Student, Group, Teacher
from user_auth.models.model_attendance import TeacherAttendance


class StudentAttendanceSerializer(serializers.ModelSerializer):
    student = serializers.PrimaryKeyRelatedField(queryset=Student.objects.all())

    class Meta:
        model = StudentAttendance
        fields = ['student', 'status']

class AttendanceCreateSerializer(serializers.Serializer):
    group = serializers.PrimaryKeyRelatedField(queryset=Group.objects.all())
    date = serializers.DateField()
    descriptions = serializers.CharField(required=False, allow_blank=True)
    attendances = serializers.DictField(
        child=serializers.ChoiceField(choices=["bor", "yo'q", "kechikkan","sababli"])
    )

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
