from rest_framework import serializers

from user_auth.models.model_payments import Payment, Month, PaymentType


# MonthSerializer - Month modelini serializatsiya qilish
class MonthSerializer(serializers.ModelSerializer):
    class Meta:
        model = Month  # Month modeli
        fields = '__all__'  # Barcha maydonlarni olish


# PaymentTypeSerializer - PaymentType modelini serializatsiya qilish
class PaymentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentType  # PaymentType modeli
        fields = '__all__'  # Barcha maydonlarni olish


# PaymentSerializer - Payment modelini serializatsiya qilish
class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment  # Payment modeli
        fields = '__all__'  # Barcha maydonlarni olish

    # Validatsiya metodini qo'llash
    def validate(self, attrs):
        student = attrs.get('student')  # Student ma'lumotini olish
        group = attrs.get('group')  # Group ma'lumotini olish

        # Agar student guruhga tegishli bo'lmasa, xatolik yuborish
        if group not in student.group.all():
            raise serializers.ValidationError("Bu student ushbu guruhga biriktirilmagan.")

        return attrs
