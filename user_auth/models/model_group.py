from django.db import models

from user_auth.models import BaseModel

class Course(BaseModel):
    title = models.CharField(max_length=50)
    descriptions = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.title

class Group(BaseModel):
    title = models.CharField(max_length=25, unique=True)
    course = models.ForeignKey('user_auth.Course', on_delete=models.RESTRICT, related_name='group_course')
    teacher = models.ManyToManyField('user_auth.Teacher',related_name="group_teacher")
    table = models.ForeignKey('user_auth.Table', on_delete=models.RESTRICT)
    start_date = models.DateField()
    end_date = models.DateField()
    descriptions = models.CharField(max_length=400, null=True, blank=True)

    def __str__(self):
        return self.title
