from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ModelViewSet

from user_auth.add_permissions import IsStaffUser
from user_auth.models import Rooms, TableType, Table
from user_auth.serializers import RoomSerializer, TableTypeSerializer, TableSerializer


class RoomsViewSet(ModelViewSet):
    queryset = Rooms.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [IsAdminUser, IsStaffUser]


class TableTypeViewSet(ModelViewSet):
    queryset = TableType.objects.all()
    serializer_class = TableTypeSerializer
    permission_classes = [IsAdminUser, IsStaffUser]


class TableViewSet(ModelViewSet):
    queryset = Table.objects.all()
    serializer_class = TableSerializer
    permission_classes = [IsAdminUser, IsStaffUser]
