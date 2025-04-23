from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAdminUser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import Group, Student, Attendance
from datetime import date

# from ..serializers import AttendanceSerializer
from ..serializers.attendance_serializer import *


class AttendanceCreateAPIView(APIView):
    @swagger_auto_schema(request_body=AttendanceCreateSerializer)
    def post(self, request):
        serializer = AttendanceCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": True, "message": "Attendance created successfully!"}, status=status.HTTP_201_CREATED)
        return Response({"success": False, "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class TeacherAttendanceCreateAPIView(APIView):
    @swagger_auto_schema(request_body=TeacherAttendanceCreateSerializer)
    def post(self, request):
        serializer = TeacherAttendanceCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": True, "message": "Attendance created successfully!"}, status=status.HTTP_201_CREATED)
        return Response({"success": False, "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
