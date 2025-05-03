from django.db.models import Sum, Avg
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from user_auth.add_permissions import IsStaffOrAdminUser
from user_auth.models import LessonAttendance, Group, Student
from user_auth.models.model_payments import Payment
from user_auth.serializers.statistics_serializer import DateRangeSerializer


# StudentsStatisticsView, belgilangan vaqt oralig'ida talabalar bo'yicha statistikani hisoblaydi
class StudentsStatisticsView(APIView):
    permission_classes = [IsStaffOrAdminUser]  # Faqat staff yoki admin foydalanuvchilari foydalanishi mumkin

    @swagger_auto_schema(request_body=DateRangeSerializer)  # API uchun Swagger hujjatlarini avtomatik yaratish
    def post(self, request):
        serializer = DateRangeSerializer(
            data=request.data)  # Kirish ma'lumotlarini (boshlanish va tugash sanasi) deserializatsiya qilish

        # Kirish sanasi va tugash sanasini tekshirish
        if serializer.is_valid():
            start_date = serializer.validated_data['start_date']
            end_date = serializer.validated_data['end_date']

            # Ro'yxatga olingan va tugatgan talabalarni olish
            registered_students = Student.objects.filter(created_ed__range=(start_date, end_date))
            finished_students = Student.objects.filter(group__end_date__range=(start_date, end_date))
            current_students = Student.objects.exclude(
                id__in=finished_students)  # Hozirgi vaqtgacha tugamagan talabalar

            # Ro'yxatga olingan talabalar uchun ma'lumot tayyorlash
            registered_data = []
            for student in registered_students:
                end_dates = student.group.values_list('end_date', flat=True)
                registered_data.append({
                    "id": student.id,
                    "username": student.fullname,
                    "created_ed": student.created_ed,
                    "finished_date": max(end_dates) if end_dates else None
                })

            # Tugallangan talabalar uchun ma'lumot tayyorlash
            graduated_data = []
            for student in finished_students:
                end_dates = student.group.values_list('end_date', flat=True)
                graduated_data.append({
                    "id": student.id,
                    "username": student.fullname,
                    "created_ed": student.created_ed,
                    "finished_date": max(end_dates) if end_dates else None
                })

            # Hozirgi talabalar uchun ma'lumot tayyorlash
            current_data = []
            for student in current_students:
                end_dates = student.group.values_list('end_date', flat=True)
                current_data.append({
                    "id": student.id,
                    "username": student.fullname,
                    "created_ed": student.created_ed,
                    "finished_date": max(end_dates) if end_dates else None
                })

            # Statistikalarning JSON shaklida javobini qaytarish
            return Response({
                "registered_students_count": len(registered_data),
                "finished_students_count": len(graduated_data),
                "current_students_count": len(current_data),
                "new_registered_students": registered_data,
                "finished_students": graduated_data,
                "current_students": current_data
            })

        # Agar serializer noto'g'ri bo'lsa, xatoliklarni qaytarish
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# LessonAttendanceStatisticsView, belgilangan guruh va vaqt oralig'ida darslar bo'yicha davomat statistikalarini hisoblaydi
class LessonAttendanceStatisticsView(APIView):
    permission_classes = [IsStaffOrAdminUser]  # Faqat staff yoki admin foydalanuvchilari foydalanishi mumkin

    @swagger_auto_schema(request_body=DateRangeSerializer)  # API uchun Swagger hujjatlarini avtomatik yaratish
    def post(self, request, pk):
        serializer = DateRangeSerializer(
            data=request.data)  # Kirish ma'lumotlarini (boshlanish va tugash sanasi) deserializatsiya qilish

        # Kirish sanasi va tugash sanasini tekshirish
        if serializer.is_valid():
            start_date = serializer.validated_data.pop("start_date")
            end_date = serializer.validated_data.pop("end_date")

            # Berilgan guruhni olish va darslar bo'yicha davomatni filtrlash
            group = Group.objects.get(pk=pk)
            lesson_attendance_qs = LessonAttendance.objects.filter(
                lesson__group=group,
                lesson__date__range=[start_date, end_date]
            ).select_related('lesson', 'student').order_by('lesson__date')

            result = {}

            # Har bir dars uchun davomatni qayd etish
            for attendance in lesson_attendance_qs:
                lesson = attendance.lesson
                lesson_title = lesson.title
                lesson_date = str(lesson.date)

                # Har bir darsni sanasi va nomi bo'yicha guruhlash
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

                # Har bir talabani ularning davomat holatiga qarab guruhlash
                if statuss == 'keldi':
                    result[key]["kelganlar"].append(student_id)
                elif statuss == 'kechikkan':
                    result[key]["kechikkanlar"].append(student_id)
                elif statuss == 'sababli':
                    result[key]["sababli"].append(student_id)
                elif statuss == 'kelmadi':
                    result[key]["kelmaganlar"].append(student_id)

            # Har bir dars uchun jami talabalar soni va foizni hisoblash
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

            # Natijalarni JSON shaklida qaytarish
            return Response(result)

        # Agar serializer noto'g'ri bo'lsa, xatoliklarni qaytarish
        return Response(data=serializer.errors)


# PaymentStatisticsView, belgilangan vaqt oralig'ida to'lovlar bo'yicha statistikani hisoblaydi
class PaymentStatisticsView(APIView):
    permission_classes = [IsStaffOrAdminUser]  # Faqat staff yoki admin foydalanuvchilari foydalanishi mumkin

    @swagger_auto_schema(request_body=DateRangeSerializer)  # API uchun Swagger hujjatlarini avtomatik yaratish
    def post(self, request):
        serializer = DateRangeSerializer(
            data=request.data)  # Kirish ma'lumotlarini (boshlanish va tugash sanasi) deserializatsiya qilish

        # Kirish sanasi va tugash sanasini tekshirish
        if serializer.is_valid():
            start_date = serializer.validated_data.pop("start_date")
            end_date = serializer.validated_data.pop("end_date")

            # Berilgan vaqt oralig'ida to'lovlarni hisoblash
            total_payments = Payment.objects.filter(created_ed__range=(start_date, end_date)).count()
            total_amount_paid = \
                Payment.objects.filter(created_ed__range=(start_date, end_date)).aggregate(total=Sum('price'))[
                    'total'] or 0
            average_payment = \
                Payment.objects.filter(created_ed__range=(start_date, end_date)).aggregate(avg=Avg('price'))['avg'] or 0

            # Talabalar bo'yicha to'lovlarni hisoblash
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

            # Natijalarni JSON shaklida qaytarish
            return Response({
                "total_payments": total_payments,
                "total_amount_paid": total_amount_paid,
                "average_payment": average_payment,
                "payments_by_student": payments_list
            })

        # Agar serializer noto'g'ri bo'lsa, xatoliklarni qaytarish
        return Response(serializer.errors, status=400)
