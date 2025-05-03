from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet

from user_auth.add_permissions import IsStaffOrAdminUser
from user_auth.models import Rooms, TableType, Table
from user_auth.serializers import RoomSerializer, TableTypeSerializer, TableSerializer


class RoomsViewSet(ModelViewSet):
    queryset = Rooms.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [IsStaffOrAdminUser]
    pagination_class = PageNumberPagination


class TableTypeViewSet(ModelViewSet):
    queryset = TableType.objects.all()
    serializer_class = TableTypeSerializer
    permission_classes = [IsStaffOrAdminUser]
    pagination_class = PageNumberPagination


class TableViewSet(ModelViewSet):
    queryset = Table.objects.all()
    serializer_class = TableSerializer
    permission_classes = [IsStaffOrAdminUser]
    pagination_class = PageNumberPagination
