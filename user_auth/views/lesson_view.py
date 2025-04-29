from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import Lesson, GroupHomeWork, HomeWork, LessonAttendance, Student
from ..serializers import LessonSerializer, LessonCreateSerializer, GroupHomeWorkSerializer, HomeWorkSerializer, \
    LessonAttendanceSerializer
from rest_framework.decorators import action

# class LessonViewSet(viewsets.ModelViewSet):
#     queryset = Lesson.objects.all()
#     serializer_class = LessonSerializer
#
#     def get_serializer_class(self):
#         if self.action == 'create':
#             return LessonCreateSerializer
#         return LessonSerializer
#
#     @action(detail=True, methods=['get'])
#     def attendances(self, request, pk=None):
#         lesson = self.get_object()
#         attendances = LessonAttendance.objects.filter(lesson=lesson)
#         serializer = LessonAttendanceSerializer(attendances, many=True)
#         return Response(serializer.data)

class LessonAttendanceViewSet(viewsets.ModelViewSet):
    queryset = LessonAttendance.objects.all()
    serializer_class = LessonAttendanceSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        lesson_id = data.get('lesson')
        student_id = data.get('student')
        status_value = data.get('status')

        # Lesson va Student obyektlarini olish
        try:
            lesson = Lesson.objects.get(id=lesson_id)
        except Lesson.DoesNotExist:
            return Response({"error": "Bunday lesson mavjud emas."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            student = Student.objects.get(id=student_id)
        except Student.DoesNotExist:
            return Response({"error": "Bunday student mavjud emas."}, status=status.HTTP_400_BAD_REQUEST)

        # LessonAttendance yaratish
        attendance = LessonAttendance.objects.create(
            lesson=lesson,
            student=student,
            status=status_value
        )

        # Serializer orqali javobni qaytarish
        serializer = self.get_serializer(attendance)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class HomeWorkViewSet(viewsets.ModelViewSet):
    queryset = HomeWork.objects.all()
    serializer_class = HomeWorkSerializer

class GroupHomeWorkViewSet(viewsets.ModelViewSet):
    queryset = GroupHomeWork.objects.all()
    serializer_class = GroupHomeWorkSerializer
#
# class LessonViewSet(viewsets.ModelViewSet):
#     queryset = Lesson.objects.all()
#     serializer_class = LessonSerializer
#
#     @action(detail=False, methods=['post'])
#     def create_lesson_with_attendance(self, request):
#         lesson_data = request.data
#         serializer = LessonSerializer(data=lesson_data)
#         if serializer.is_valid():
#             lesson = serializer.save()
#
#             # Attendance yaratish
#             attendance_serializer = LessonAttendanceCreateSerializer(data=lesson_data)
#             if attendance_serializer.is_valid():
#                 attendance_serializer.save()
#                 return Response({
#                     'lesson': serializer.data,
#                     'attendance': attendance_serializer.data
#                 }, status=status.HTTP_201_CREATED)
#             else:
#                 return Response(attendance_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

class LessonCreateWithAttendance(APIView):
    print("Salom")
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
                'start_time': lesson.start_time,
                'end_time': lesson.end_time,
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

class LessonWithAttendanceGet(APIView):
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





#
# class LessonAttendanceView(APIView):
#     def post(self,request):
#         serializer = LessonAttendanceCreateSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()

