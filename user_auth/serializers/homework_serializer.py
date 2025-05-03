from rest_framework import serializers

from user_auth.models import HomeWork, GroupHomeWork, HomeworkReview


# HomeWorkSerializer - HomeWork modelini serializatsiya qilish
class HomeWorkSerializer(serializers.ModelSerializer):
    is_checked = serializers.BooleanField(read_only=True)
    student = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = HomeWork  # HomeWork modeli
        fields = ['id', 'group_homework', 'student', 'link', 'descriptions','is_checked']  # Tanlangan maydonlar


# GroupHomeWorkSerializer - GroupHomeWork modelini serializatsiya qilish
class GroupHomeWorkSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupHomeWork  # GroupHomeWork modeli
        fields = '__all__'  # Barcha maydonlarni olish


# HomeworkReviewSerializer - HomeworkReview modelini serializatsiya qilish
class HomeworkReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = HomeworkReview  # HomeworkReview modeli
        fields = '__all__'  # Barcha maydonlarni olish
