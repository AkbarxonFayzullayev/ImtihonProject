from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from user_auth.add_permissions import IsStaffOrAdminUser
from user_auth.models.model_payments import Payment, PaymentType, Month
from user_auth.serializers.payments_serializer import PaymentSerializer, PaymentTypeSerializer, MonthSerializer


# Month'lar ro'yxatini olish va yangi oy qo'shish uchun API
class MonthApi(APIView):
    permission_classes = [IsStaffOrAdminUser]

    # Barcha month obyektlarini olish
    @swagger_auto_schema(responses={200: MonthSerializer(many=True)})
    def get(self, request):
        month = Month.objects.all()
        serializer = MonthSerializer(month, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    # Yangi month qo'shish
    @swagger_auto_schema(request_body=MonthSerializer)
    def post(self, request):
        serializer = MonthSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        return Response(data=serializer.errors)


# Bitta Month bilan CRUD ishlari
class MonthDetail(APIView):
    permission_classes = [IsStaffOrAdminUser]

    # Bitta month obyektini olish
    @swagger_auto_schema(responses={200: MonthSerializer()})
    def get(self, request, pk):
        month = get_object_or_404(Month, pk=pk)
        serializer = MonthSerializer(month)
        return Response(data=serializer.data)

    # Month obyektini to'liq yangilash
    @swagger_auto_schema(request_body=MonthSerializer)
    def put(self, request, pk):
        month = get_object_or_404(Month, pk=pk)
        serializer = MonthSerializer(month, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Month obyektini qisman yangilash
    @swagger_auto_schema(request_body=MonthSerializer)
    def patch(self, request, pk):
        month = get_object_or_404(Month, pk=pk)
        serializer = MonthSerializer(month, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Month obyektini o'chirish
    @swagger_auto_schema(responses={204: "Successfully deleted"})
    def delete(self, request, pk):
        month = get_object_or_404(Month, pk=pk)
        month.delete()
        return Response(data={"detail": "Month o'chirildi"}, status=204)


# PaymentType'lar ro'yxati va yangi tur qo'shish uchun API
class PaymentTypeApi(APIView):
    permission_classes = [IsStaffOrAdminUser]

    @swagger_auto_schema(responses={200: PaymentTypeSerializer(many=True)})
    def get(self, request):
        payment_type = PaymentType.objects.all()
        serializer = PaymentTypeSerializer(payment_type, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=PaymentTypeSerializer)
    def post(self, request):
        serializer = PaymentTypeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        return Response(data=serializer.errors)


# Bitta PaymentType bilan CRUD ishlari
class PaymentTypeDetail(APIView):
    permission_classes = [IsStaffOrAdminUser]

    @swagger_auto_schema(responses={200: PaymentTypeSerializer()})
    def get(self, request, pk):
        payment_type = get_object_or_404(PaymentType, pk=pk)
        serializer = PaymentTypeSerializer(payment_type)
        return Response(data=serializer.data)

    @swagger_auto_schema(request_body=PaymentTypeSerializer)
    def put(self, request, pk):
        payment_type = get_object_or_404(PaymentType, pk=pk)
        serializer = PaymentTypeSerializer(payment_type, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=PaymentTypeSerializer)
    def patch(self, request, pk):
        payment_type = get_object_or_404(PaymentType, pk=pk)
        serializer = PaymentTypeSerializer(payment_type, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(responses={204: "Successfully deleted"})
    def delete(self, request, pk):
        payment_type = get_object_or_404(PaymentType, pk=pk)
        payment_type.delete()
        return Response(data={"detail": "Payment Type o'chirildi"}, status=204)


# Barcha to'lovlar ro'yxatini olish va yangi to'lov qo'shish
class PaymentApi(APIView):
    permission_classes = [IsStaffOrAdminUser]

    @swagger_auto_schema(responses={200: PaymentSerializer(many=True)})
    def get(self, request):
        payments = Payment.objects.all()
        serializer = PaymentSerializer(payments, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=PaymentSerializer)
    def post(self, request):
        serializer = PaymentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        return Response(data=serializer.errors)


# Bitta to'lov bilan CRUD ishlari
class PaymentDetail(APIView):
    permission_classes = [IsStaffOrAdminUser]

    @swagger_auto_schema(responses={200: PaymentSerializer()})
    def get(self, request, pk):
        payments = get_object_or_404(Payment, pk=pk)
        serializer = PaymentSerializer(payments)
        return Response(data=serializer.data)

    @swagger_auto_schema(request_body=PaymentSerializer)
    def put(self, request, pk):
        payments = get_object_or_404(Payment, pk=pk)
        serializer = PaymentSerializer(payments, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=PaymentSerializer)
    def patch(self, request, pk):
        payments = get_object_or_404(Payment, pk=pk)
        serializer = PaymentSerializer(payments, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(responses={204: "Successfully deleted"})
    def delete(self, request, pk):
        payments = get_object_or_404(Payment, pk=pk)
        payments.delete()
        return Response(data={"detail": "Payment o'chirildi"}, status=204)
