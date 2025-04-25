from rest_framework import serializers

from user_auth.models import HomeWork, GroupHomeWork


class HomeWorkSerializer(serializers.ModelSerializer):
    class Meta:
        model = HomeWork
        fields = '__all__'


class GroupHomeWorkSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupHomeWork
        fields = '__all__'
