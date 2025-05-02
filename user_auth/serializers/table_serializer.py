from rest_framework import serializers

from user_auth.models import Rooms, TableType, Table


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rooms
        fields = '__all__'


class TableTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TableType
        fields = ['id', 'title', 'descriptions']


class TableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = ['id', 'start_time', 'end_time', 'room', 'type', 'descriptions']
