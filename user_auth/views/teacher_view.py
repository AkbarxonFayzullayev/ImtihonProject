from django.db.models.fields import return_None
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from user_auth.add_permissions import IsTeacherUser, IsStaffOrAdminUser
from ..models import Group, GroupHomeWork, Student, HomeWork, LessonAttendance, Lesson
from ..models.model_teacher import *
from ..serializers import TeacherSerializer, TeacherPostSerializer, DepartmentsSerializer, GroupTitleUpdateForTeacher
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema


# Teacher_Api, o'qituvchilarni boshqarish uchun API
class Teacher_Api(APIView):
    permission_classes = [IsStaffOrAdminUser]  # Faqat staff yoki admin foydalanuvchilariga ruxsat

    # Barcha o'qituvchilarni olish
    @swagger_auto_schema(
        responses={200: TeacherSerializer(many=True)}
    )
    def get(self, request):
        teachers = Teacher.objects.all()  # Barcha o'qituvchilarni olish
        serializer = TeacherSerializer(teachers, many=True)  # O'qituvchilarni serializatsiya qilish
        return Response(serializer.data)

    # Yangi o'qituvchi yaratish
    @swagger_auto_schema(request_body=TeacherPostSerializer)
    def post(self, request):
        serializer = TeacherPostSerializer(data=request.data)  # Ma'lumotlarni serializerga uzatish
        if serializer.is_valid():
            serializer.save()  # Yangi o'qituvchini saqlash
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)  # Yangi o'qituvchi yaratildi
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # Xatolik yuz berdi


# TeacherDetail, o'qituvchining batafsil ma'lumotlarini olish va yangilash uchun API
class TeacherDetail(APIView):
    permission_classes = [IsStaffOrAdminUser]  # Faqat staff yoki admin foydalanuvchilariga ruxsat

    # O'qituvchining ma'lumotlarini olish
    @swagger_auto_schema(responses={200: TeacherPostSerializer()})
    def get(self, request, pk):
        teacher = get_object_or_404(Teacher, pk=pk)  # ID bo'yicha o'qituvchini olish
        serializer = TeacherPostSerializer(teacher)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # O'qituvchini to'liq yangilash
    @swagger_auto_schema(request_body=TeacherPostSerializer)
    def put(self, request, pk):
        teacher = get_object_or_404(Teacher, pk=pk)  # ID bo'yicha o'qituvchini olish
        serializer = TeacherPostSerializer(teacher, data=request.data)  # Yangilash uchun ma'lumot
        if serializer.is_valid():
            serializer.save()  # O'qituvchini yangilash
            return Response(data=serializer.data)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # O'qituvchini qisman yangilash
    @swagger_auto_schema(request_body=TeacherPostSerializer)
    def patch(self, request, pk):
        teacher = get_object_or_404(Teacher, pk=pk)  # ID bo'yicha o'qituvchini olish
        serializer = TeacherPostSerializer(teacher, data=request.data, partial=True)  # Qisman yangilash
        if serializer.is_valid():
            serializer.save()  # O'qituvchini qisman yangilash
            return Response(data=serializer.data)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # O'qituvchini o'chirish
    @swagger_auto_schema(responses={204: 'Deleted successfully', 404: 'Not Found'})
    def delete(self, request, pk):
        try:
            teacher = Teacher.objects.get(pk=pk)  # O'qituvchini olish
        except Teacher.DoesNotExist:
            raise NotFound("Bunday ID ga ega Teacher topilmadi. ")  # O'qituvchi topilmasa xato
        teacher.user.delete()  # O'qituvchining foydalanuvchi hisobini o'chirish
        teacher.delete()  # O'qituvchini o'chirish
        return Response({"detail": "Teacher va unga tegishli User o'chirildi"}, status=204)


# DepartmentsViewSet, bo'limlarni boshqarish uchun ViewSet
class DepartmentsViewSet(ModelViewSet):
    queryset = Departments.objects.all()  # Barcha bo'limlarni olish
    serializer_class = DepartmentsSerializer  # Bo'limlarni serializatsiya qilish
    permission_classes = [IsStaffOrAdminUser]  # Faqat staff yoki admin foydalanuvchilari uchun
    pagination_class = PageNumberPagination  # Sahifalashni qo'llash


# TeacherGetGroups, o'qituvchining guruhlarini olish uchun API
class TeacherGetGroups(APIView):
    permission_classes = [IsTeacherUser]  # Faqat o'qituvchilarga ruxsat

    def get(self, request):
        user = request.user
        teacher = Teacher.objects.get(user=user)  # Hozirgi foydalanuvchini o'qituvchi sifatida olish
        groups = Group.objects.filter(teacher=teacher)  # O'qituvchiga tegishli guruhlarni olish

        response = []
        for group in groups:
            response.append({
                "id": group.id,
                "title": group.title,
                "start_date": group.start_date,
                "end_date": group.end_date,
                "course": group.course.title if group.course else None,
                "student_count": group.students.count()  # Guruhdagi o'quvchilar soni
            })

        return Response(response)


# TeacherGetGroupStudents, o'qituvchining guruhidagi o'quvchilarni olish uchun API
class TeacherGetGroupStudents(APIView):
    permission_classes = [IsTeacherUser]  # Faqat o'qituvchilarga ruxsat

    def get(self, request):
        user = request.user
        teacher = get_object_or_404(Teacher, user=user)  # O'qituvchini olish
        groups = Group.objects.filter(teacher=teacher)  # O'qituvchiga tegishli guruhlarni olish

        response = []
        for group in groups:
            students_data = []
            for student in group.students.all():  # Guruhdagi barcha o'quvchilarni olish
                students_data.append({
                    "id": student.id,
                    "fullname": student.fullname,
                    "phone_number": student.user.phone_number  # O'quvchining telefon raqami
                })

            response.append({
                "id": group.id,
                "title": group.title,
                "student_count": group.students.count(),  # Guruhdagi o'quvchilar soni
                "students": students_data  # O'quvchilarning ro'yxati
            })

        return Response(response)

class TeacherGetHomeworkStatistic(APIView):
    permission_classes = [IsTeacherUser]

    def get(self, request):
        user = request.user
        if not user.is_teacher:
            return Response({"detail": "Faqat o‘qituvchilar uchun."}, status=403)

        try:
            teacher = Teacher.objects.get(user=user)
        except Teacher.DoesNotExist:
            return Response({"detail": "Teacher topilmadi."}, status=404)

        teacher_groups = Group.objects.filter(teacher=teacher)
        group_homeworks = GroupHomeWork.objects.filter(group__in=teacher_groups).select_related('group', 'lesson')

        result = []

        for hw in group_homeworks:
            all_students = Student.objects.filter(group=hw.group)
            submitted_ids = HomeWork.objects.filter(group_homework=hw).values_list('student', flat=True)

            submitted_students = all_students.filter(id__in=submitted_ids)
            not_submitted_students = all_students.exclude(id__in=submitted_ids)

            submitted_dict = {s.id: s.fullname for s in submitted_students}
            not_submitted_dict = {s.id: s.fullname for s in not_submitted_students}

            total = all_students.count()
            done = submitted_students.count()
            percent = round((done / total) * 100, 2) if total > 0 else 0

            result.append({
                "homework_id": hw.id,
                "title": hw.title,
                "group_name": hw.group.title,
                "submitted_students": submitted_dict,
                "not_submitted_students": not_submitted_dict,
                "percent_done": percent
            })

        return Response(result)

class TeacherGetAttendanceStatistic(APIView):
    permission_classes = [IsTeacherUser]

    def get(self, request):
        teacher = Teacher.objects.get(user=request.user)
        groups = Group.objects.filter(teacher=teacher)
        lessons = Lesson.objects.filter(group__in=groups)

        data = []
        for lesson in lessons:
            attendances = LessonAttendance.objects.filter(lesson=lesson).select_related('student')
            kelganlar = {}
            kelmaganlar = {}
            kechikkanlar = {}
            sabablilar = {}

            for att in attendances:
                if att.status == "bor":
                    kelganlar[att.student.id] = att.student.fullname
                elif att.status == "yo'q":
                    kelmaganlar[att.student.id] = att.student.fullname
                elif att.status == "kechikkan":
                    kechikkanlar[att.student.id] = att.student.fullname
                elif att.status == "sababli":
                    sabablilar[att.student.id] = att.student.fullname

            data.append({
                "lesson_id": lesson.id,
                "group": lesson.group.title,
                "date": lesson.date,
                "lesson": lesson.title,
                "kelganlar": kelganlar,
                "kelmaganlar": kelmaganlar,
                "kechikkanlar": kechikkanlar,
                "sabablilar": sabablilar
            })

        return Response(data)

class TeacherUpdateGroupTitle(APIView):
    permission_classes = [IsTeacherUser]
    @swagger_auto_schema(request_body=GroupTitleUpdateForTeacher)
    def patch(self,request,pk):
        user = request.user
        teacher = Teacher.objects.get(user=user)
        groups = Group.objects.filter(teacher__in=[teacher])
        try:
            group = Group.objects.get(id__in=groups,pk=pk)
        except Exception:
            return Response({"detail": "guruh sizga tegishli emas yozki topilmadi"})

        serializer = GroupTitleUpdateForTeacher(group,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"detail":"Guruh title muvaffaqiyatli o'zgartirildi. "})