from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import UpdateAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from ..add_permissions import IsTeacherOrStaffOrAdmin
from ..models import Lesson, LessonAttendance
from ..serializers.lesson_serializer import LessonAttendanceSerializer, LessonCreateSerializer, LessonSerializer, \
    LessonUpdateSerializer


class LessonCreateWithAttendance(APIView):
    permission_classes = [IsTeacherOrStaffOrAdmin]

    @swagger_auto_schema(request_body=LessonCreateSerializer)
    def post(self, request):
        lesson_data = request.data
        lesson_serializer = LessonCreateSerializer(data=lesson_data)
        if lesson_serializer.is_valid():
            lesson = lesson_serializer.save()

            # Lesson ni qayta serialize qilamiz
            lesson_info = {
                'id': lesson.id,
                'title': lesson.title,
                'group': lesson.group.id,
                'date': lesson.date,
                'table': lesson.table.id,
                'descriptions': lesson.descriptions,
            }

            # Attendance ma'lumotlarini tayyorlash
            attendances = LessonAttendance.objects.filter(lesson=lesson)
            attendance_list = []
            for attendance in attendances:
                attendance_list.append({
                    'student_id': attendance.student.id,
                    'status': attendance.status
                })

            return Response({
                'lesson': lesson_info,
                'attendances': attendance_list
            }, status=status.HTTP_201_CREATED)
        else:
            return Response(lesson_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AllLessonList(APIView):
    permission_classes = [IsTeacherOrStaffOrAdmin]

    def get(self, request):
        lessons = Lesson.objects.all()
        result = []

        for lesson in lessons:
            kelgan = []
            kelmagan = []
            sababli = []
            kechikkan = []

            attendances = LessonAttendance.objects.filter(lesson=lesson)
            for attendance in attendances:
                student_id = attendance.student.id
                if attendance.status == "keldi":
                    kelgan.append(student_id)
                elif attendance.status == "kelmadi":
                    kelmagan.append(student_id)
                elif attendance.status == "sababli":
                    sababli.append(student_id)
                elif attendance.status == "kechikkan":
                    kechikkan.append(student_id)

            result.append({
                "lesson_id": lesson.id,
                "title": lesson.title,
                "group": lesson.group.id,
                "date": lesson.date,
                "kelgan_studentlar": kelgan,
                "kelmagan_studentlar": kelmagan,
                "sababli_studentlar": sababli,
                "kechikkan_studentlar": kechikkan
            })

        return Response(result)


class LessonWithAttendanceGet(APIView):
    permission_classes = [IsTeacherOrStaffOrAdmin]

    def get(self, request, pk):
        try:
            lesson = Lesson.objects.get(pk=pk)
        except Lesson.DoesNotExist:
            return Response({"error": "Lesson topilmadi"}, status=404)

        attendances = LessonAttendance.objects.filter(lesson=lesson)

        kelgan = []
        kelmagan = []
        sababli = []
        kechikkan = []

        for attendance in attendances:
            student_id = attendance.student.id

            if attendance.status == "keldi":
                kelgan.append(student_id)
            elif attendance.status == "kelmadi":
                kelmagan.append(student_id)
            elif attendance.status == "sababli":
                sababli.append(student_id)
            elif attendance.status == "kechikkan":
                kechikkan.append(student_id)

        data = {
            "lesson_id": lesson.id,
            "title": lesson.title,
            "group": lesson.group.id,
            "date": lesson.date,
            "kelgan_studentlar": kelgan,
            "kelmagan_studentlar": kelmagan,
            "sababli_studentlar": sababli,
            "kechikkan_studentlar": kechikkan
        }

        return Response(data, status=200)


class UpdateLessonView(UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsTeacherOrStaffOrAdmin]


class DeleteLessonView(APIView):
    permission_classes = [IsTeacherOrStaffOrAdmin]

    def delete(self, request, pk):
        try:
            lesson = Lesson.objects.get(pk=pk)
        except Lesson.DoesNotExist:
            return Response({"error": "Bunday ID li Dars mavjud emas! "}, status=status.HTTP_400_BAD_REQUEST)
        attendances = LessonAttendance.objects.filter(lesson=lesson)
        attendances.delete()
        lesson.delete()
        return Response({"success": "Dars va unga tegishli davomatlar o‘chirildi!"}, status=status.HTTP_204_NO_CONTENT)


class AttendanceUpdateView(APIView):
    permission_classes = [IsTeacherOrStaffOrAdmin]

    @swagger_auto_schema(request_body=LessonAttendanceSerializer)
    def put(self, request, pk):
        try:
            attendance = LessonAttendance.objects.get(pk=pk)
        except LessonAttendance.DoesNotExist:
            return Response({"error": "Bunday ID li davomat topilmadi"})
        serializer = LessonAttendanceSerializer(attendance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=LessonAttendanceSerializer)
    def patch(self, request, pk):
        try:
            attendance = LessonAttendance.objects.get(pk=pk)
        except LessonAttendance.DoesNotExist:
            return Response({"error": "Bunday ID li davomat topilmadi"})
        serializer = LessonAttendanceSerializer(attendance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LessonFullUpdateView(APIView):
    permission_classes = [IsTeacherOrStaffOrAdmin]

    @swagger_auto_schema(request_body=LessonUpdateSerializer)
    def put(self, request, pk):
        try:
            lesson = Lesson.objects.get(pk=pk)
        except Lesson.DoesNotExist:
            return Response({"error": "Bunday ID li Lesson topilmadi."}, status=status.HTTP_404_NOT_FOUND)

        serializer = LessonUpdateSerializer(lesson, data=request.data)
        if serializer.is_valid():
            updated_lesson = serializer.save()
            return Response(LessonSerializer(updated_lesson).data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=LessonUpdateSerializer)
    def patch(self, request, pk):
        try:
            lesson = Lesson.objects.get(pk=pk)
        except Lesson.DoesNotExist:
            return Response({"error": "Bunday ID li Lesson topilmadi."}, status=status.HTTP_404_NOT_FOUND)

        serializer = LessonUpdateSerializer(lesson, data=request.data, partial=True)
        if serializer.is_valid():
            updated_lesson = serializer.save()
            return Response(LessonSerializer(updated_lesson).data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
