from rest_framework import serializers

from user_auth.models.model_payments import Payments


class PaymentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payments
        fields = '__all__'

