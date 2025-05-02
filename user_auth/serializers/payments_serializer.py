from rest_framework import serializers

from user_auth.models.model_payments import Payment, Month, PaymentType


class MonthSerializer(serializers.ModelSerializer):
    class Meta:
        model = Month
        fields = '__all__'


class PaymentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentType
        fields = '__all__'


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'

    def validate(self, attrs):
        student = attrs.get('student')
        group = attrs.get('group')

        if group not in student.group.all():
            raise serializers.ValidationError("Bu student ushbu guruhga biriktirilmagan.")

        return attrs
