from rest_framework import serializers

from user_auth.models import HomeWork, GroupHomeWork, HomeworkReview


class HomeWorkSerializer(serializers.ModelSerializer):
    class Meta:
        model = HomeWork
        fields = ['id', 'group_homework', 'student', 'link', 'descriptions', ]


class GroupHomeWorkSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupHomeWork
        fields = '__all__'


class HomeworkReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = HomeworkReview
        fields = '__all__'
