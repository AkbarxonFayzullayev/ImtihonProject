
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import Group, Student, Attendance
from datetime import date
from ..serializers.attendance_serializer import *


class AttendanceCreateAPIView(APIView):
    # @swagger_auto_schema(responses={200:AttendanceListSerializer(many=True)})
    # def get(self, request):
    #     attendances = Attendance.objects.all().order_by('-date')  # eng oxirgi davomat birinchi bo‘lsin
    #     serializer = AttendanceListSerializer(attendances, many=True)
    #     return Response(serializer.data)
    @swagger_auto_schema(request_body=AttendanceCreateSerializer)
    def post(self, request):
        serializer = AttendanceCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": True, "message": "Attendance created successfully!"},
                            status=status.HTTP_201_CREATED)
        return Response({"success": False, "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class AttendanceUpdateAPIView(APIView):
    @swagger_auto_schema(request_body=AttendanceCreateSerializer)
    def put(self, request, pk):
        attendance = get_object_or_404(Attendance, pk=pk)
        # Serializerda instance ni beradi va to‘liq yangilanish uchun data yuboriladi
        serializer = AttendanceCreateSerializer(instance=attendance, data=request.data)
        if serializer.is_valid():
            serializer.save()  # Bu yerda butun Attendance modelini yangilaydi
            return Response({"success": True, "message": "Attendance updated!"})
        return Response(serializer.errors, status=400)

    @swagger_auto_schema(request_body=AttendanceCreateSerializer)
    def patch(self, request, pk):
        attendance = get_object_or_404(Attendance, pk=pk)
        serializer = AttendanceCreateSerializer(instance=attendance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": True, "message": "Attendance updated!"})
        return Response(serializer.errors, status=400)

    @swagger_auto_schema(responses={204: "Attendance deleted"})
    def delete(self, request, pk):
        attendance = get_object_or_404(Attendance, pk=pk)
        attendance.delete()
        return Response({"success": True, "message": "Attendance deleted!"}, status=204)


class StudentAttendanceView(APIView):
    def get(self, request, id):
        # Studentni ID-si orqali olish
        try:
            student = Student.objects.get(id=id)
        except Student.DoesNotExist:
            return Response({"error": "Student topilmadi"}, status=404)

        # StudentAttendance modelidan o'quvchining barcha davomatlarini olish
        student_attendances = StudentAttendance.objects.filter(student=student).select_related('attendance')

        # Serializer yordamida javobni qaytarish
        serializer = StudentAttendanceSerializer(student_attendances, many=True)
        return Response(serializer.data)


class StudentRequestAttendanceView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        if not user.is_student == True:
            return Response({"error": "Siz student emassiz"}, status=403)

        student = user.student

        student_attendances = StudentAttendance.objects.filter(
            student=student).select_related('attendance').order_by('-attendance__date')

        serializer = StudentAttendanceSerializer(student_attendances, many=True)
        return Response(serializer.data)


class TeacherAttendanceCreateAPIView(APIView):
    @swagger_auto_schema(request_body=TeacherAttendanceCreateSerializer)
    def post(self, request):
        serializer = TeacherAttendanceCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": True, "message": "Attendance created successfully!"},
                            status=status.HTTP_201_CREATED)
        return Response({"success": False, "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class TeacherAttendanceDetail(APIView):
    def get(self, request, pk=None):
        if pk:
            # ID orqali ma'lum bir TeacherAttendance olish
            try:
                attendance = TeacherAttendance.objects.get(pk=pk)
            except TeacherAttendance.DoesNotExist:
                return Response({"error": "TeacherAttendance not found"}, status=404)
            serializer = TeacherAttendanceSerializer(attendance)
            return Response(serializer.data)
        else:
            # Barcha TeacherAttendancelarni olish
            attendances = TeacherAttendance.objects.all()
            serializer = TeacherAttendanceSerializer(attendances, many=True)
            return Response(serializer.data)

    def put(self, request, pk):
        try:
            attendance = TeacherAttendance.objects.get(pk=pk)
        except TeacherAttendance.DoesNotExist:
            return Response({"error": "TeacherAttendance not found"}, status=404)

        serializer = TeacherAttendanceCreateSerializer(instance=attendance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": True, "message": "Attendance updated!"})
        return Response(serializer.errors, status=400)

    # Partially Update: TeacherAttendanceni qisman yangilash
    @swagger_auto_schema(request_body=TeacherAttendanceCreateSerializer)
    def patch(self, request, pk):
        try:
            attendance = TeacherAttendance.objects.get(pk=pk)
        except TeacherAttendance.DoesNotExist:
            return Response({"error": "TeacherAttendance not found"}, status=404)

        serializer = TeacherAttendanceCreateSerializer(instance=attendance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": True, "message": "Attendance updated!"})
        return Response(serializer.errors, status=400)

    # Delete: TeacherAttendance o'chirish
    @swagger_auto_schema(responses={204: "TeacherAttendance deleted"})
    def delete(self, request, pk):
        try:
            attendance = TeacherAttendance.objects.get(pk=pk)
        except TeacherAttendance.DoesNotExist:
            return Response({"error": "TeacherAttendance not found"}, status=404)

        attendance.delete()
        return Response({"success": True, "message": "Attendance deleted!"}, status=204)


class AllAttendanceList(APIView):

    def get(self, request):
        attendances = Attendance.objects.prefetch_related('student_attendances__student', 'group').all()
        serializer = AttendanceListSerializer(attendances, many=True)
        return Response(serializer.data)
