from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import Group, Student, Attendance
from datetime import date

# from ..serializers import AttendanceSerializer
from ..serializers.attendance_serializer import *

#
# class AttendanceView(APIView):
#     @swagger_auto_schema(request_body=AttendanceSerializer)
#     def post(self, request):
#         group_id = request.data.get("group_id")
#         attendance_data = request.data.get("attendance", {})
#
#         if not group_id or not attendance_data:
#             return Response(
#                 {"success": False, "message": "group_id va attendance ma'lumotlari kerak"},
#                 status=status.HTTP_400_BAD_REQUEST
#             )
#
#         try:
#             group = Group.objects.get(id=group_id)
#         except Group.DoesNotExist:
#             return Response(
#                 {"success": False, "message": "Guruh topilmadi"},
#                 status=status.HTTP_404_NOT_FOUND
#             )
#
#         students = group.students.all()
#         today = date.today()
#         created = []
#
#         for student in students:
#             status_ = attendance_data.get(str(student.id))
#             if status_ not in ["bor", "yo'q", "kechikkan"]:
#                 continue  # noto‘g‘ri statuslar tashlab ketiladi
#
#             att = Attendance(
#                 student=student,
#                 group=group,
#                 date=today,
#                 status=status_
#             )
#             att.save()
#             created.append(att.id)
#
#         return Response(
#             {"success": True, "message": "Davomat saqlandi", "count": len(created)},
#             status=status.HTTP_201_CREATED
#         )

# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from user_auth.serializers.attendance_serializer import GroupAttendanceSerializer
#
# class GroupAttendanceCreateAPIView(APIView):
#     def post(self, request):
#         serializer = GroupAttendanceSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({"success": True, "message": "Davomat saqlandi"}, status=status.HTTP_201_CREATED)
#         return Response({"success": False, "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class AttendanceCreateAPIView(APIView):
    @swagger_auto_schema(request_body=AttendanceCreateSerializer)
    def post(self, request):
        serializer = AttendanceCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": True, "message": "Attendance created successfully!"}, status=status.HTTP_201_CREATED)
        return Response({"success": False, "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
