from rest_framework import serializers

from user_auth.models import Group, Course


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course  # Course modelini serializatsiya qilish
        fields = '__all__'  # Barcha maydonlarni serializatsiya qilish


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group  # Group modelini serializatsiya qilish
        fields = '__all__'  # Barcha maydonlarni serializatsiya qilish
