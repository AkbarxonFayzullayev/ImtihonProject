from rest_framework import serializers

from user_auth.models import Rooms, TableType, Table


# RoomSerializer - Rooms modelini serializatsiya qilish
class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rooms  # Rooms modeli
        fields = '__all__'  # Barcha maydonlarni olish


# TableTypeSerializer - TableType modelini serializatsiya qilish
class TableTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TableType  # TableType modeli
        fields = ['id', 'title', 'descriptions']  # Kerakli maydonlar


# TableSerializer - Table modelini serializatsiya qilish
class TableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table  # Table modeli
        fields = ['id', 'start_time', 'end_time', 'room', 'type', 'descriptions']  # Kerakli maydonlar
