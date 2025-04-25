from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from user_auth.models import Student
from user_auth.serializers import StudentSerializer
from user_auth.serializers.statistics_serializer import DateRangeSerializer


class Mock_data(APIView):
    @swagger_auto_schema(request_body=DateRangeSerializer)
    def post(self, request):
        serializer = DateRangeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        start_date = serializer.validated_data['start_date']
        end_date = serializer.validated_data['end_date']

        # Ro‘yxatdan o‘tganlar
        registered_students = Student.objects.filter(
            created_ed__range=(start_date, end_date)
        )

        # Bitirganlar
        finished_students = Student.objects.filter(
            group__end_date__range=(start_date, end_date)
        )


        data = {
            "registered_count": registered_students.count(),
            "finished_count": finished_students.count(),
            "registered_students": StudentSerializer(registered_students, many=True).data,
            "finished_students": StudentSerializer(finished_students, many=True).data
        }

        return Response(data, status=status.HTTP_200_OK)