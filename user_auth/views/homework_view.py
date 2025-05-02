from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from user_auth.add_permissions import IsTeacherUser, IsStaffUser, IsStudentUser
from user_auth.models import  HomeworkReview, GroupHomeWork, \
    HomeWork
from user_auth.serializers import  HomeworkReviewSerializer, \
    GroupHomeWorkSerializer, HomeWorkSerializer


class GroupHomeWorkAPIView(APIView):
    permission_classes = [IsTeacherUser,IsStaffUser,IsAdminUser,IsStudentUser]
    def get(self, request):
        homeworks = GroupHomeWork.objects.all()
        serializer = GroupHomeWorkSerializer(homeworks, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=GroupHomeWorkSerializer)
    def post(self, request):
        self.permission_classes = [IsTeacherUser]
        serializer = GroupHomeWorkSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GroupHomeWorkDetailView(APIView):
    def get(self, request, pk):
        self.permission_classes = [IsStudentUser,IsTeacherUser,IsStaffUser,IsAdminUser]
        try:
            group_homework = GroupHomeWork.objects.get(pk=pk)
        except GroupHomeWork.DoesNotExist:
            return Response({"error": "Bunday ID li GroupHomework topilmadi."}, status=status.HTTP_400_BAD_REQUEST)
        serializer = GroupHomeWorkSerializer(group_homework)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=GroupHomeWorkSerializer)
    def put(self, request, pk):
        self.permission_classes = [IsTeacherUser]
        try:
            group_homework = GroupHomeWork.objects.get(pk=pk)
        except GroupHomeWork.DoesNotExist:
            return Response({"error": "Bunday ID li GroupHomework topilmadi."}, status=status.HTTP_400_BAD_REQUEST)
        serializer = GroupHomeWorkSerializer(group_homework, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=GroupHomeWorkSerializer)
    def patch(self, request, pk):
        self.permission_classes = [IsTeacherUser]
        try:
            group_homework = GroupHomeWork.objects.get(pk=pk)
        except GroupHomeWork.DoesNotExist:
            return Response({"error": "Bunday ID li GroupHomework topilmadi."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = GroupHomeWorkSerializer(group_homework, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        self.permission_classes = [IsTeacherUser]
        try:
            homework = GroupHomeWork.objects.get(pk=pk)
        except HomeWork.DoesNotExist:
            return Response({"error": "Bunday ID li GroupHomeWork topilmadi."}, status=status.HTTP_400_BAD_REQUEST)
        homework.delete()
        return Response({"success": "GroupHomeWork o‘chirildi."}, status=status.HTTP_204_NO_CONTENT)


# HomeWork
class HomeWorkAPIView(APIView):

    def get(self, request):
        self.permission_classes = [IsTeacherUser, IsStudentUser, IsStaffUser, IsAdminUser]
        homeworks = HomeWork.objects.all()
        serializer = HomeWorkSerializer(homeworks, many=True)
        return Response(data=serializer.data)

    @swagger_auto_schema(request_body=HomeWorkSerializer)
    def post(self, request):
        self.permission_classes = [IsStudentUser]
        serializer = HomeWorkSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class HomeWorkDetailView(APIView):
    permission_classes = [IsStudentUser,IsTeacherUser]
    def get(self, request, pk):
        self.permission_classes = [IsStaffUser,IsAdminUser,IsTeacherUser]
        try:
            homework = HomeWork.objects.get(pk=pk)
        except HomeWork.DoesNotExist:
            return Response({"error": "Bunday ID li HomeWork topilmadi."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = HomeWorkSerializer(homework)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=HomeWorkSerializer)
    def put(self, request, pk):
        self.permission_classes = [IsStudentUser]
        try:
            homework = HomeWork.objects.get(pk=pk)
        except HomeWork.DoesNotExist:
            return Response({"error": "Bunday ID li HomeWork topilmadi."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = HomeWorkSerializer(homework, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=HomeWorkSerializer)
    def patch(self, request, pk):
        self.permission_classes = [IsStudentUser]
        try:
            homework = HomeWork.objects.get(pk=pk)
        except HomeWork.DoesNotExist:
            return Response({"error": "Bunday ID li HomeWork topilmadi."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = HomeWorkSerializer(homework, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=HomeWorkSerializer)
    def delete(self, request, pk):
        self.permission_classes = [IsStudentUser]
        try:
            homework = HomeWork.objects.get(pk=pk)
        except HomeWork.DoesNotExist:
            return Response({"error": "Bunday ID li HomeWork topilmadi."}, status=status.HTTP_400_BAD_REQUEST)

        homework.delete()
        return Response({"success": "HomeWork o‘chirildi."}, status=status.HTTP_204_NO_CONTENT)


# HomeworkReview
class HomeworkReviewAPIView(APIView):
    def get(self, request):
        self.permission_classes = [IsTeacherUser,IsAdminUser,IsStaffUser]
        homework_reviews = HomeworkReview.objects.all()
        serializer = HomeworkReviewSerializer(homework_reviews, many=True)
        return Response(data=serializer.data)

    @swagger_auto_schema(request_body=HomeworkReviewSerializer)
    def post(self, request):
        self.permission_classes = [IsTeacherUser]
        serializer = HomeworkReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            # Homework is_checked = True update
            homework = serializer.validated_data['homework']
            homework.is_checked = True
            homework.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class HomeworkReviewDetailView(APIView):

    def get(self, request, pk):
        self.permission_classes = [IsTeacherUser,IsStaffUser,IsAdminUser]
        try:
            review = HomeworkReview.objects.get(pk=pk)
        except HomeworkReview.DoesNotExist:
            return Response({"error": "Bunday ID li HomeworkReview topilmadi."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = HomeworkReviewSerializer(review)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=HomeworkReviewSerializer)
    def put(self, request, pk):
        self.permission_classes = [IsTeacherUser]
        try:
            review = HomeworkReview.objects.get(pk=pk)
        except HomeworkReview.DoesNotExist:
            return Response({"error": "Bunday ID li HomeworkReview topilmadi."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = HomeworkReviewSerializer(review, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=HomeworkReviewSerializer)
    def patch(self, request, pk):
        self.permission_classes = [IsTeacherUser]
        try:
            review = HomeworkReview.objects.get(pk=pk)
        except HomeworkReview.DoesNotExist:
            return Response({"error": "Bunday ID li HomeworkReview topilmadi."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = HomeworkReviewSerializer(review, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(responses={204: "Homework o'chirildi"})
    def delete(self, request, pk):
        self.permission_classes = [IsTeacherUser]
        try:
            review = HomeworkReview.objects.get(pk=pk)
        except HomeworkReview.DoesNotExist:
            return Response({"error": "Bunday ID li HomeworkReview topilmadi."}, status=status.HTTP_400_BAD_REQUEST)

        review.delete()
        return Response({"success": "HomeworkReview o‘chirildi."}, status=status.HTTP_204_NO_CONTENT)
