from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet

from user_auth.add_permissions import IsStaffOrAdminUser
from user_auth.models import Rooms, TableType, Table
from user_auth.serializers import RoomSerializer, TableTypeSerializer, TableSerializer


# RoomsViewSet, xona ma'lumotlarini boshqarish uchun ViewSet
class RoomsViewSet(ModelViewSet):
    queryset = Rooms.objects.all()  # Xonalar ro'yxatini olish
    serializer_class = RoomSerializer  # Xonalarni serializatsiya qilish uchun serializer
    permission_classes = [IsStaffOrAdminUser]  # Faqat staff yoki admin foydalanuvchilari uchun
    pagination_class = PageNumberPagination  # Sahifalashni qo'llash


# TableTypeViewSet, stol turini boshqarish uchun ViewSet
class TableTypeViewSet(ModelViewSet):
    queryset = TableType.objects.all()  # Stol turini olish
    serializer_class = TableTypeSerializer  # Stol turini serializatsiya qilish uchun serializer
    permission_classes = [IsStaffOrAdminUser]  # Faqat staff yoki admin foydalanuvchilari uchun
    pagination_class = PageNumberPagination  # Sahifalashni qo'llash


# TableViewSet, stol ma'lumotlarini boshqarish uchun ViewSet
class TableViewSet(ModelViewSet):
    queryset = Table.objects.all()  # Stollar ro'yxatini olish
    serializer_class = TableSerializer  # Stollarni serializatsiya qilish uchun serializer
    permission_classes = [IsStaffOrAdminUser]  # Faqat staff yoki admin foydalanuvchilari uchun
    pagination_class = PageNumberPagination  # Sahifalashni qo'llash
