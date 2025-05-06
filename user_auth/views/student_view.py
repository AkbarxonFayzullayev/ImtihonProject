from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from user_auth.add_permissions import IsStudentUser, IsStaffOrAdminUser
from ..models import Student, Parents, HomeWork, HomeworkReview, LessonAttendance
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema

from ..models.model_payments import Payment
from ..serializers.student_serilalizer import StudentSerializer, StudentPostSerializer, ParentsSerializer


# Student_Api, barcha talabalar ro'yxatini olish va yangi talaba qo'shish uchun API
class Student_Api(APIView):
    permission_classes = [IsStaffOrAdminUser]  # Faqat staff yoki admin foydalanuvchilari uchun

    @swagger_auto_schema(
        responses={200: StudentSerializer(many=True)}  # Barcha talabalar uchun serializatsiya javobi
    )
    def get(self, request):
        students = Student.objects.all()  # Barcha studentlarni olish
        serializer = StudentSerializer(students, many=True)  # Serializatsiya qilish
        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=StudentPostSerializer  # Yangi student ma'lumotlari kiritilishi
    )
    def post(self, request):
        serializer = StudentPostSerializer(data=request.data)  # Yangi talaba qo'shish
        if serializer.is_valid():
            serializer.save()  # Yangi talabani saqlash
            return Response(data=serializer.data)
        return Response(data=serializer.errors)  # Agar noto'g'ri bo'lsa, xatoliklarni qaytarish


# StudentDetail, o'quvchining detalini ko'rish, yangilash, o'zgartirish va o'chirish
class StudentDetail(APIView):
    permission_classes = [IsStaffOrAdminUser]  # Faqat staff yoki admin foydalanuvchilari uchun

    @swagger_auto_schema(responses={200: StudentPostSerializer()})  # Talaba ma'lumotlarini ko'rish
    def get(self, request, pk):
        student = get_object_or_404(Student, pk=pk)  # Talaba ID orqali topiladi
        serializer = StudentSerializer(student)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=StudentPostSerializer)  # Talaba ma'lumotlarini yangilash
    def put(self, request, pk):
        student = get_object_or_404(Student, pk=pk)  # Talaba ID orqali topiladi
        serializer = StudentPostSerializer(student, data=request.data)
        if serializer.is_valid():
            serializer.save()  # Yangilanishlarni saqlash
            return Response(data=serializer.data)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=StudentPostSerializer)  # Talaba ma'lumotlarini qisman yangilash
    def patch(self, request, pk):
        student = get_object_or_404(Student, pk=pk)  # Talaba ID orqali topiladi
        serializer = StudentPostSerializer(student, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()  # Qisman yangilanishlarni saqlash
            return Response(data=serializer.data)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(responses={204: 'Deleted successfully', 404: 'Not Found'})  # Talaba o'chirish
    def delete(self, request, pk):
        try:
            student = Student.objects.get(pk=pk)  # Talaba ID orqali topiladi
        except Student.DoesNotExist:
            raise NotFound("Bunday ID ga ega Student topilmadi. ")  # Agar talaba topilmasa, xatolik
        student.user.delete()  # Talaba bilan bog'liq foydalanuvchi o'chiriladi
        student.delete()  # Talaba o'chiriladi
        return Response({"detail": "Student va unga tegishli User o'chirildi"}, status=204)


# ParentsViewSet, ota-onalar ma'lumotlarini boshqarish uchun ViewSet
class ParentsViewSet(ModelViewSet):
    permission_classes = [IsStaffOrAdminUser]  # Faqat staff yoki admin foydalanuvchilari uchun
    queryset = Parents.objects.all()  # Ota-onalar ma'lumotlari
    serializer_class = ParentsSerializer  # Serializer sinfi


# StudentGetHomeworks, talaba uchun uy vazifalarini olish
class StudentGetHomeworks(APIView):
    permission_classes = [IsStudentUser]  # Faqat talabalar uchun

    def get(self, request):
        user = request.user
        student = Student.objects.get(user=user)  # Foydalanuvchi orqali talaba obyekti
        groups = student.group.all()  # Talabaga tegishli guruhlar
        homeworks = HomeWork.objects.filter(group_homework__group__in=groups)  # Talabaga biriktirilgan guruhlarga tegishli uy vazifalari

        data = []
        for homework in homeworks:
            try:
                # Har bir uy vazifasi uchun baho va izohni olish
                review = homework.homeworkreview
                score = review.score  # Baholash ballari
                comment = review.comment  # Izoh
            except HomeworkReview.DoesNotExist:
                score = None
                comment = None

            # Agar uy vazifasi tekshirilmagan bo'lsa, 'is_checked' False bo'ladi
            is_checked = homework.is_checked if homework.is_checked else False

            data.append({
                "homework_title": homework.group_homework.title,
                "descriptions": homework.descriptions,
                "link": homework.link,
                "is_checked": is_checked,
                "deadline": homework.group_homework.deadline,
                "score": score,
                "review_comment": comment
            })

        return Response(data)  # Barcha uy vazifalari ma'lumotlari qaytariladi



# StudentGetAttendance, talaba uchun davomat ma'lumotlarini olish
class StudentGetAttendance(APIView):
    permission_classes = [IsStudentUser]  # Faqat talabalar uchun

    def get(self, request):
        user = request.user
        student = Student.objects.get(user=user)  # Foydalanuvchi orqali talaba obyekti
        attendances = LessonAttendance.objects.filter(student=student).select_related('lesson')  # Talabaning davomati

        data = []
        for attendance in attendances:
            data.append({
                "lesson_title": attendance.lesson.title,
                "lesson_date": attendance.lesson.date,
                "group": attendance.lesson.group.title,
                "status": attendance.status,
            })

        return Response(data)  # Davomat ma'lumotlarini qaytarish


# StudentGetPayments, talaba to'lovlari haqida ma'lumot olish
class StudentGetPayments(APIView):
    permission_classes = [IsStudentUser]  # Faqat talabalar uchun

    def get(self, request):
        user = request.user
        student = Student.objects.get(user=user)  # Foydalanuvchi orqali talaba obyekti
        payments = Payment.objects.filter(student=student)  # Talabaning to'lovlari

        data = []
        for payment in payments:
            data.append({
                "payment_id": payment.id,
                "month": payment.month.title,
                "group_id": payment.group.id,
                "group_title": payment.group.title,
                "course_title": payment.group.course.title,
                "type": payment.payment_type.title,
                "price": payment.price,
            })

        return Response(data)  # To'lovlar haqida ma'lumotlar
