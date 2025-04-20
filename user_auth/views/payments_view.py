from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from user_auth.models.model_payments import Payments
from user_auth.serializers.payments_serializer import PaymentsSerializer

class PaymentsApi(APIView):
    @swagger_auto_schema(responses={200: PaymentsSerializer(many=True)})
    def get(self,request):
        payments = Payments.objects.all()
        serializer = PaymentsSerializer(payments,many=True)
        return Response(data=serializer.data,status=status.HTTP_200_OK)
    @swagger_auto_schema(request_body=PaymentsSerializer)
    def post(self,request):
        serializer = PaymentsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        return Response(data=serializer.errors)
