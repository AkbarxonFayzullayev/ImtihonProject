from rest_framework import serializers


# class AttendanceStatisticSerializer(serializers.Serializer):
#     group = serializers.CharField()
#     total_students = serializers.IntegerField()
#     present = serializers.IntegerField()
#     absent = serializers.IntegerField()
#     late = serializers.IntegerField()
#     total_percentage = serializers.FloatField()
#
#
# class CourseStatisticSerializer(serializers.Serializer):
#     course_name = serializers.CharField()
#     total_groups = serializers.IntegerField()
#     total_students = serializers.IntegerField()
#
#
# class GroupStatisticSerializer(serializers.Serializer):
#     group_name = serializers.CharField()
#     course = serializers.CharField()
#     total_students = serializers.IntegerField()
#
#
# class PaymentsStatisticSerializer(serializers.Serializer):
#     total_payments = serializers.IntegerField()
#     total_amount = serializers.DecimalField(max_digits=10, decimal_places=2)
#     average_payment = serializers.DecimalField(max_digits=10, decimal_places=2)
#
#
# class StudentStatisticSerializer(serializers.Serializer):
#     total_students = serializers.IntegerField()
#     active_student = serializers.IntegerField()
#
#
# class TeacherStatisticSerializer(serializers.Serializer):
#     teacher_name = serializers.CharField()
#     total_groups = serializers.IntegerField()
#     total_students = serializers.IntegerField()


class DateRangeSerializer(serializers.Serializer):
    start_date = serializers.DateField()
    end_date = serializers.DateField()
