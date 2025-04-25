from django.contrib.staticfiles.views import serve
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from user_auth.models.model_payments import Payment, PaymentType, Month
from user_auth.serializers.payments_serializer import PaymentSerializer, PaymentTypeSerializer, MonthSerializer


class MonthApi(APIView):
    @swagger_auto_schema(responses={200: MonthSerializer(many=True)})
    def get(self,request):
        month = Month.objects.all()
        serializer = MonthSerializer(month,many=True)
        return Response(data=serializer.data,status=status.HTTP_200_OK)
    @swagger_auto_schema(request_body=PaymentTypeSerializer)
    def post(self,request):
        serializer = MonthSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        return Response(data=serializer.errors)

class MonthDetail(APIView):
    @swagger_auto_schema(responses={200:MonthSerializer()})
    def get(self,request,pk):
        month = get_object_or_404(Month,pk=pk)
        serializer = MonthSerializer(month)
        return Response(data=serializer.data)

    @swagger_auto_schema(request_body=MonthSerializer)
    def put(self,request,pk):
        month = get_object_or_404(Month,pk=pk)
        serializer = MonthSerializer(month,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        return Response(data=serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=PaymentTypeSerializer)
    def patch(self, request, pk):
        month = get_object_or_404(Month, pk=pk)
        serializer = PaymentTypeSerializer(month, data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(responses={204:"Successfully deleted"})
    def delete(self,request,pk):
        month = get_object_or_404(Month,pk=pk)
        month.delete()
        return Response(data={"detail":"Month o'chirildi"},status=204)


class PaymentTypeApi(APIView):
    @swagger_auto_schema(responses={200: PaymentTypeSerializer(many=True)})
    def get(self,request):
        payment_type = PaymentType.objects.all()
        serializer = PaymentTypeSerializer(payment_type,many=True)
        return Response(data=serializer.data,status=status.HTTP_200_OK)
    @swagger_auto_schema(request_body=PaymentTypeSerializer)
    def post(self,request):
        serializer = PaymentTypeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        return Response(data=serializer.errors)

class PaymentTypeDetail(APIView):
    @swagger_auto_schema(responses={200:PaymentTypeSerializer()})
    def get(self,request,pk):
        payment_type = get_object_or_404(PaymentType,pk=pk)
        serializer = PaymentTypeSerializer(payment_type)
        return Response(data=serializer.data)

    @swagger_auto_schema(request_body=PaymentTypeSerializer)
    def put(self,request,pk):
        payment_type = get_object_or_404(PaymentType,pk=pk)
        serializer = PaymentTypeSerializer(payment_type,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        return Response(data=serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=PaymentTypeSerializer)
    def patch(self, request, pk):
        payment_type = get_object_or_404(PaymentType, pk=pk)
        serializer = PaymentTypeSerializer(payment_type, data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(responses={204:"Successfully deleted"})
    def delete(self,request,pk):
        payment_type = get_object_or_404(PaymentType,pk=pk)
        payment_type.delete()
        return Response(data={"detail":"Payment Type o'chirildi"},status=204)

class PaymentApi(APIView):
    @swagger_auto_schema(responses={200: PaymentSerializer(many=True)})
    def get(self,request):
        payments = Payment.objects.all()
        serializer = PaymentSerializer(payments,many=True)
        return Response(data=serializer.data,status=status.HTTP_200_OK)
    @swagger_auto_schema(request_body=PaymentSerializer)
    def post(self,request):
        serializer = PaymentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        return Response(data=serializer.errors)

class PaymentDetail(APIView):
    @swagger_auto_schema(responses={200:PaymentSerializer()})
    def get(self,request,pk):
        payments = get_object_or_404(Payment,pk=pk)
        serializer = PaymentSerializer(payments)
        return Response(data=serializer.data)

    @swagger_auto_schema(request_body=PaymentSerializer)
    def put(self,request,pk):
        payments = get_object_or_404(Payment,pk=pk)
        serializer = PaymentSerializer(payments,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        return Response(data=serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=PaymentSerializer)
    def patch(self, request, pk):
        payments = get_object_or_404(Payment, pk=pk)
        serializer = PaymentSerializer(payments, data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(responses={204:"Successfully deleted"})
    def delete(self,request,pk):
        payments = get_object_or_404(Payment,pk=pk)
        payments.delete()
        return Response(data={"detail":"Payment o'chirildi"},status=204)
