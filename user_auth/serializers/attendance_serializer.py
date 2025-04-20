# # from rest_framework import serializers
# #
# # from user_auth.models import Attendance
# #
# # class AttendanceSerializer(serializers.ModelSerializer):
# #     class Meta:
# #         model = Attendance
# #         fields = ['id', 'group', 'student', 'date', 'status', 'descriptions']
# #
# #     def validate_status(self, value):
# #         if value not in ['present', 'absent', 'late']:
# #             raise serializers.ValidationError("Status noto'g'ri.")
# #         return value
# from rest_framework import serializers
# from ..models import Attendance, Group, Student
#
# class AttendanceSerializer(serializers.Serializer):
#     group_id = serializers.IntegerField()
#     date = serializers.DateField()
#     descriptions = serializers.CharField(required=False, allow_blank=True)
#     attendances = serializers.DictField(
#         child=serializers.ChoiceField(choices=["bor", "yo'q", "kechikkan"])
#     )
#
#     def validate_group_id(self, value):
#         if not Group.objects.filter(id=value).exists():
#             raise serializers.ValidationError("Bunday group mavjud emas")
#         return value
#
#     def validate_attendances(self, value):
#         if not value:
#             raise serializers.ValidationError("Hech qanday o‘quvchi uchun davomat yo‘q")
#         return value
#
#     def create(self, validated_data):
#         group = Group.objects.get(id=validated_data['group_id'])
#         date_ = validated_data['date']
#         descriptions = validated_data.get('descriptions', '')
#         attendances_data = validated_data['attendances']
#
#         students = group.students.all()
#         bulk_objs = []
#
#         for student in students:
#             status_ = attendances_data.get(str(student.id))
#             if status_ not in ['bor', "yo'q", "kechikkan"]:
#                 continue
#
#             bulk_objs.append(Attendance(
#                 student=student,
#                 group=group,
#                 date=date_,
#                 status=status_,
#                 descriptions=descriptions
#             ))
#
#         # Avval eski davomatlar bo‘lsa, o‘chirib tashlaymiz
#         Attendance.objects.filter(group=group, date=date_).delete()
#         Attendance.objects.bulk_create(bulk_objs)
#
#         return bulk_objs
# from rest_framework import serializers
# from user_auth.models import Attendance, Student, Group
#
# class AttendanceItemSerializer(serializers.Serializer):
#     student_id = serializers.IntegerField()
#     status = serializers.ChoiceField(choices=['bor', 'yoq', 'kechikkan'])
#
# class GroupAttendanceSerializer(serializers.Serializer):
#     group_id = serializers.IntegerField()
#     date = serializers.DateField()
#     descriptions = serializers.CharField(required=False)
#     attendances = AttendanceItemSerializer(many=True)
#
#     def validate(self, data):
#         if not data.get('group_id') or not data.get('attendances'):
#             raise serializers.ValidationError("group_id va attendance ma'lumotlari kerak")
#         return data
#
#     def create(self, validated_data):
#         group_id = validated_data['group_id']
#         date = validated_data['date']
#         descriptions = validated_data.get('descriptions', '')
#
#         attendance_data = validated_data['attendances']
#         attendance_objects = []
#
#         for item in attendance_data:
#             attendance_objects.append(Attendance(
#                 student_id=item['student_id'],
#                 group_id=group_id,
#                 date=date,
#                 descriptions=descriptions,
#                 status=item['status']
#             ))
#         Attendance.objects.bulk_create(attendance_objects)
#         return {"success": True, "message": "Attendance saved"}
from rest_framework import serializers
from user_auth.models import Attendance, StudentAttendance, Student, Group

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
        child=serializers.ChoiceField(choices=["bor", "yo'q", "kechikkan"])
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
