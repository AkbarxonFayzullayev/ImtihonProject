from django.db.models import Sum, Avg
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from user_auth.add_permissions import IsStaffOrAdminUser
from user_auth.models import LessonAttendance, Group, Student
from user_auth.models.model_payments import Payment
from user_auth.serializers.statistics_serializer import DateRangeSerializer


class StudentsStatisticsView(APIView):
    permission_classes = [IsStaffOrAdminUser]

    @swagger_auto_schema(request_body=DateRangeSerializer)
    def post(self, request):
        serializer = DateRangeSerializer(data=request.data)
        if serializer.is_valid():
            start_date = serializer.validated_data['start_date']
            end_date = serializer.validated_data['end_date']

            registered_students = Student.objects.filter(created_ed__range=(start_date, end_date))

            finished_students = Student.objects.filter(group__end_date__range=(start_date, end_date))

            current_students = Student.objects.exclude(id__in=finished_students)

            registered_data = []
            for student in registered_students:
                end_dates = student.group.values_list('end_date', flat=True)
                registered_data.append({
                    "id": student.id,
                    "username": student.fullname,
                    "created_ed": student.created_ed,
                    "finished_date": max(end_dates) if end_dates else None
                })

            graduated_data = []
            for student in finished_students:
                end_dates = student.group.values_list('end_date', flat=True)
                graduated_data.append({
                    "id": student.id,
                    "username": student.fullname,
                    "created_ed": student.created_ed,
                    "finished_date": max(end_dates) if end_dates else None
                })

            current_data = []
            for student in current_students:
                end_dates = student.group.values_list('end_date', flat=True)
                current_data.append({
                    "id": student.id,
                    "username": student.fullname,
                    "created_ed": student.created_ed,
                    "finished_date": max(end_dates) if end_dates else None
                })

            return Response({
                "registered_students_count": len(registered_data),
                "finished_students_count": len(graduated_data),
                "current_students_count": len(current_data),
                "new_registered_students": registered_data,
                "finished_students": graduated_data,
                "current_students": current_data
            })

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LessonAttendanceStatisticsView(APIView):
    permission_classes = [IsStaffOrAdminUser]

    @swagger_auto_schema(request_body=DateRangeSerializer)
    def post(self, request, pk):
        serializer = DateRangeSerializer(data=request.data)
        if serializer.is_valid():
            start_date = serializer.validated_data.pop("start_date")
            end_date = serializer.validated_data.pop("end_date")

            group = Group.objects.get(pk=pk)

            lesson_attendance_qs = LessonAttendance.objects.filter(
                lesson__group=group,
                lesson__date__range=[start_date, end_date]
            ).select_related('lesson', 'student').order_by('lesson__date')

            result = {}

            for attendance in lesson_attendance_qs:
                lesson = attendance.lesson
                lesson_title = lesson.title
                lesson_date = str(lesson.date)

                key = f"{lesson_date} - {lesson_title}"
                if key not in result:
                    result[key] = {
                        "kelganlar": [],
                        "kechikkanlar": [],
                        "sababli": [],
                        "kelmaganlar": [],
                        "foiz": 0,
                        "jami_oquvchilar": 0,
                    }

                statuss = attendance.status
                student_id = attendance.student.id

                if statuss == 'keldi':
                    result[key]["kelganlar"].append(student_id)
                elif statuss == 'kechikkan':
                    result[key]["kechikkanlar"].append(student_id)
                elif statuss == 'sababli':
                    result[key]["sababli"].append(student_id)
                elif statuss == 'kelmadi':
                    result[key]["kelmaganlar"].append(student_id)

            for key, value in result.items():
                jami = (
                        len(value["kelganlar"])
                        + len(value["kechikkanlar"])
                        + len(value["sababli"])
                        + len(value["kelmaganlar"])
                )
                keldi = len(value["kelganlar"])
                value["jami_oquvchilar"] = jami
                value["foiz"] = round((keldi / jami) * 100, 2) if jami else 0

            return Response(result)

        return Response(data=serializer.errors)


class PaymentStatisticsView(APIView):
    permission_classes = [IsStaffOrAdminUser]

    @swagger_auto_schema(request_body=DateRangeSerializer)
    def post(self, request):
        serializer = DateRangeSerializer(data=request.data)
        if serializer.is_valid():
            start_date = serializer.validated_data.pop("start_date")
            end_date = serializer.validated_data.pop("end_date")

            total_payments = Payment.objects.filter(created_ed__range=(start_date, end_date)).count()
            total_amount_paid = \
                Payment.objects.filter(created_ed__range=(start_date, end_date)).aggregate(total=Sum('price'))[
                    'total'] or 0
            average_payment = \
                Payment.objects.filter(created_ed__range=(start_date, end_date)).aggregate(avg=Avg('price'))['avg'] or 0

            payments_by_student = Payment.objects.filter(created_ed__range=(start_date, end_date)) \
                .values('month__title', 'student__id', 'student__fullname', 'student__group__title').annotate(
                total_paid=Sum('price')).order_by('-total_paid')

            payments_list = [
                {
                    "id": item['student__id'],
                    "group": item['student__group__title'],
                    "month": item['month__title'],
                    "fullname": item['student__fullname'],
                    "total_paid": item['total_paid']
                }
                for item in payments_by_student
            ]

            return Response({
                "total_payments": total_payments,
                "total_amount_paid": total_amount_paid,
                "average_payment": average_payment,
                "payments_by_student": payments_list
            })
        return Response(serializer.errors, status=400)
