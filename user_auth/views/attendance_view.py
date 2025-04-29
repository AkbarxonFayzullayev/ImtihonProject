# from django.shortcuts import get_object_or_404
# from drf_yasg.utils import swagger_auto_schema
# from rest_framework.permissions import IsAdminUser, IsAuthenticated
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from ..models import Group, Student, LessonAttendance
# from datetime import date
# from ..serializers.attendance_serializer import *
#
# # class StudentRequestAttendanceView(APIView):
# #     permission_classes = [IsAuthenticated]
# #
# #     def get(self, request):
# #         user = request.user
# #         if not user.is_student == True:
# #             return Response({"error": "Siz student emassiz"}, status=403)
# #
# #         student = user.student
# #
# #         student_attendances = StudentAttendance.objects.filter(
# #             student=student).select_related('attendance').order_by('-attendance__date')
# #
# #         serializer = StudentAttendanceSerializer(student_attendances, many=True)
# #         return Response(serializer.data)
# #
# #
# # class TeacherAttendanceCreateAPIView(APIView):
# #     @swagger_auto_schema(request_body=TeacherAttendanceCreateSerializer)
# #     def post(self, request):
# #         serializer = TeacherAttendanceCreateSerializer(data=request.data)
# #         if serializer.is_valid():
# #             serializer.save()
# #             return Response({"success": True, "message": "Attendance created successfully!"},
# #                             status=status.HTTP_201_CREATED)
# #         return Response({"success": False, "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
#
# # class AllAttendanceList(APIView):
# #
# #     def get(self, request):
# #         attendances = Attendance.objects.prefetch_related('student_attendances__student', 'group').all()
# #         serializer = AttendanceListSerializer(attendances, many=True)
# #         return Response(serializer.data)
# # views.py
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# # from ..serializers import AttendanceCreateSerializer, AttendanceSerializer
#
#
# class AttendanceCreateView(APIView):
#     @swagger_auto_schema(request_body=AttendanceCreateSerializer)
#     def post(self, request):
#         serializer = AttendanceCreateSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({"message": "Davomat saqlandi!"}, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
# class GroupAttendanceView(APIView):
#     def get(self, request, group_id):
#         # group_id orqali barcha shu guruhga oid davomatlarni olish
#         attendances = LessonAttendance.objects.filter(group_id=group_id)
#
#         if not attendances.exists():
#             return Response({"detail": "Bu guruh uchun davomat topilmadi."}, status=404)
#
#         # date lar bo'yicha to'plab chiqamiz
#         result = {}
#
#         for attendance in attendances:
#             date_str = attendance.date.strftime("%Y-%m-%d")
#
#             if date_str not in result:
#                 result[date_str] = {
#                     "group": attendance.group.title,
#                     "date": date_str,
#                     "kelgan_studentlar": [],
#                     "sababli_studentlar": [],
#                     "kechikkan_studentlar": [],
#                     "kelmagan_studentlar": []
#                 }
#
#             if attendance.status == 'keldi':
#                 result[date_str]["kelgan_studentlar"].append(attendance.student.id)
#             elif attendance.status == 'sababli':
#                 result[date_str]["sababli_studentlar"].append(attendance.student.id)
#             elif attendance.status == 'kechikkan':
#                 result[date_str]["kechikkan_studentlar"].append(attendance.student.id)
#             elif attendance.status == 'kelmadi':
#                 result[date_str]["kelmagan_studentlar"].append(attendance.student.id)
#         return Response(result)
#
# class AttendanceUpdateView(APIView):
#     @swagger_auto_schema(request_body=AttendanceSerializer)
#     def put(self, request, pk):
#         try:
#             attendance = LessonAttendance.objects.get(pk=pk)
#         except LessonAttendance.DoesNotExist:
#             return Response({"detail": "Davomat topilmadi."}, status=status.HTTP_404_NOT_FOUND)
#
#         status_value = request.data.get('status')
#         if status_value not in ['keldi', 'kelmadi', 'sababli', 'kechikkan']:
#             return Response({"detail": "Noto'g'ri status yuborildi."}, status=status.HTTP_400_BAD_REQUEST)
#
#         attendance.status = status_value
#         attendance.save()
#
#         return Response({"detail": "Davomat muvaffaqiyatli yangilandi."}, status=status.HTTP_200_OK)
