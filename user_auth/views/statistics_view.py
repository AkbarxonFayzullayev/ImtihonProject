from datetime import date

from django.db.models import Sum, Avg
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response

from user_auth.models import Course, Group, Student, Teacher, Attendance
from rest_framework.views import APIView

from user_auth.models.model_payments import Payment
from user_auth.serializers.statistics_serializer import AttendanceStatisticSerializer, TeacherStatisticSerializer, \
    StudentStatisticSerializer, PaymentsStatisticSerializer, GroupStatisticSerializer, CourseStatisticSerializer, \
    DateRangeSerializer


class AttendanceStatisticsView(APIView):
    def get(self, request):
        today = date.today()
        attendances = Attendance.objects.filter(date=today)

        statistics = []
        for attendance in attendances:
            student_attendances = attendance.student_attendances.all()
            total_students = student_attendances.count()
            present = student_attendances.filter(status='bor').count()
            absent = student_attendances.filter(status="yo'q").count()
            late = student_attendances.filter(status='kechikkan').count()

            percentage = (present / total_students) * 100 if total_students else 0

            statistics.append({
                'group': attendance.group.title,
                'total_students': total_students,
                'present': present,
                'absent': absent,
                'late': late,
                'total_percentage': round(percentage, 2)
            })

        serializer = AttendanceStatisticSerializer(statistics, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=DateRangeSerializer)
    def post(self, request):
        serializer = DateRangeSerializer(data=request.data)
        if serializer.is_valid():
            start_date = serializer.validated_data["start_date"]
            end_date = serializer.validated_data["end_date"]
            attendances = Attendance.objects.filter(date__range=[start_date, end_date])

            statistics = []
            for attendance in attendances:
                student_attendances = attendance.student_attendances.all()
                total_students = student_attendances.count()
                present = student_attendances.filter(status='bor').count()
                absent = student_attendances.filter(status="yo'q").count()
                late = student_attendances.filter(status='kechikkan').count()

                percentage = (present / total_students) * 100 if total_students else 0

                statistics.append({
                    'group': attendance.group.title,
                    'total_students': total_students,
                    'present': present,
                    'absent': absent,
                    'late': late,
                    'total_percentage': round(percentage, 2)
                })

            serializer = AttendanceStatisticSerializer(statistics, many=True)
            return Response(serializer.data)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CourseStatisticsView(APIView):
    @swagger_auto_schema(responses={200: CourseStatisticSerializer(many=True)})
    def get(self, request):
        courses = Course.objects.all()
        data = []

        for course in courses:
            groups = Group.objects.filter(course=course)
            students_count = sum(group.get_student_group.count() for group in groups)

            data.append({
                "course_name": course.title,
                "total_groups": groups.count(),
                "total_students": students_count
            })

        return Response(data)


class GroupStatisticsView(APIView):
    @swagger_auto_schema(responses={200: GroupStatisticSerializer(many=True)})
    def get(self, request):
        groups = Group.objects.all()
        data = []

        for group in groups:
            data.append({
                "group_title": group.title,
                "course_title": group.course.title,
                "start_date": group.start_date,
                "end_date": group.end_date,
                "total_students": group.get_student_group.count(),
            })
        return Response(data=data, status=status.HTTP_200_OK)


class PaymentsStatisticsView(APIView):
    @swagger_auto_schema(responses={200: PaymentsStatisticSerializer(many=True)})
    def get(self, request):
        total = Payment.objects.aggregate(
            total_payments=Sum('amount'),
            average_payment=Avg('amount')
        )

        data = {
            "total_payments": Payment.objects.count(),
            "total_amount": total['total_payments'] or 0,
            "average_payment": total['average_payment'] or 0
        }

        return Response(data)


class StudentStatisticsView(APIView):
    @swagger_auto_schema(responses={200: StudentStatisticSerializer(many=True)})
    def get(self, post):
        total = Student.objects.count()
        active = Student.objects.filter(is_line=True).count()

        data = {
            "total_students": total,
            "active_students": active
        }
        return Response(data)


class TeacherStatisticsView(APIView):
    @swagger_auto_schema(responses={200: TeacherStatisticSerializer(many=True)})
    def get(self, request):
        teachers = Teacher.objects.all()
        data = []

        for teacher in teachers:
            groups = teacher.group_teacher.all()
            student_count = sum(group.students.count() for group in groups)

            data.append({
                "teacher_name": teacher.user.phone_number,
                "total_groups": groups.count(),
                "total_students": student_count
            })

            return Response(data)
