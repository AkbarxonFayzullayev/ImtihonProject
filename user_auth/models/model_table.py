from django.db import models

from user_auth.models import BaseModel


class Rooms(BaseModel):
    title = models.CharField(max_length=50)
    descriptions = models.CharField(max_length=400, null=True, blank=True)

    def __str__(self):
        return self.title


class TableType(models.Model):
    title = models.CharField(max_length=50)
    descriptions = models.CharField(max_length=400, null=True, blank=True)

    def __str__(self):
        return self.title



class Table(BaseModel):
    start_time = models.TimeField()
    end_time = models.TimeField()
    room = models.ForeignKey('user_auth.Rooms', on_delete=models.RESTRICT)
    type = models.ForeignKey('user_auth.TableType', on_delete=models.RESTRICT)
    descriptions = models.CharField(max_length=500, null=True, blank=True)
