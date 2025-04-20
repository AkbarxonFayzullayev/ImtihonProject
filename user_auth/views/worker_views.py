from rest_framework.viewsets import ModelViewSet

from user_auth.models import Worker
from user_auth.serializers import WorkerSerializer


class WorkerViewSet(ModelViewSet):
    queryset = Worker.objects.all()
    serializer_class = WorkerSerializer
