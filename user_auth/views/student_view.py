from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from user_auth.add_permissions import IsStudentUser, IsStaffOrAdminUser
from ..models import Student, Parents, HomeWork, HomeworkReview, LessonAttendance
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema

from ..models.model_payments import Payment
from ..serializers.student_serilalizer import StudentSerializer, StudentPostSerializer, ParentsSerializer


class Student_Api(APIView):
    permission_classes = [IsStaffOrAdminUser]

    @swagger_auto_schema(
        responses={200: StudentSerializer(many=True)}
    )
    def get(self, request):
        students = Student.objects.all()  # Barcha studentlarni olish
        serializer = StudentSerializer(students, many=True)  # Serializatsiya qilish
        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=StudentPostSerializer
    )
    def post(self, request):
        serializer = StudentPostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        return Response(data=serializer.errors)


class StudentDetail(APIView):
    permission_classes = [IsStaffOrAdminUser]

    @swagger_auto_schema(responses={200: StudentPostSerializer()})
    def get(self, request, pk):
        student = get_object_or_404(Student, pk=pk)
        serializer = StudentSerializer(student)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=StudentPostSerializer)
    def put(self, request, pk):
        student = get_object_or_404(Student, pk=pk)
        serializer = StudentPostSerializer(student, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=StudentPostSerializer)
    def patch(self, request, pk):
        student = get_object_or_404(Student, pk=pk)
        serializer = StudentPostSerializer(student, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(responses={204: 'Deleted successfully', 404: 'Not Found'})
    def delete(self, request, pk):
        try:
            student = Student.objects.get(pk=pk)
        except Student.DoesNotExist:
            raise NotFound("Bunday ID ga ega Teacher topilmadi. ")
        student.user.delete()
        student.delete()
        return Response({"detail": "Teacher va unga tegishli User o'chirildi"}, status=204)


class ParentsViewSet(ModelViewSet):
    permission_classes = [IsStaffOrAdminUser]
    queryset = Parents.objects.all()
    serializer_class = ParentsSerializer


class StudentGetHomeworks(APIView):
    permission_classes = [IsStudentUser]

    def get(self, request):
        user = request.user
        student = Student.objects.get(user=user)
        homeworks = HomeWork.objects.filter(student=student)

        data = []
        for homework in homeworks:
            try:
                review = homework.homeworkreview
                score = review.score
                comment = review.comment
            except HomeworkReview.DoesNotExist:
                score = None
                comment = None

            data.append({
                "homework_title": homework.group_homework.title,
                "descriptions": homework.descriptions,
                "link": homework.link,
                "is_checked": homework.is_checked,
                "deadline": homework.group_homework.deadline,
                "score": score,
                "review_comment": comment
            })

        return Response(data)


class StudentGetAttendance(APIView):
    permission_classes = [IsStudentUser]

    def get(self, request):
        user = request.user
        student = Student.objects.get(user=user)
        attendances = LessonAttendance.objects.filter(student=student).select_related('lesson')

        data = []
        for attendance in attendances:
            data.append({
                "lesson_title": attendance.lesson.title,
                "lesson_date": attendance.lesson.date,
                "group": attendance.lesson.group.title,
                "status": attendance.status,
            })

        return Response(data)


class StudentGetPayments(APIView):
    permission_classes = [IsStudentUser]

    def get(self, request):
        user = request.user
        student = Student.objects.get(user=user)
        payments = Payment.objects.filter(student=student)

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

        return Response(data)
