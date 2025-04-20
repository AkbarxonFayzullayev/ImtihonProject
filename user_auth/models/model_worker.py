from django.db import models
from user_auth.models import BaseModel


class Worker(BaseModel):
    user = models.OneToOneField('user_auth.User', on_delete=models.CASCADE)
    departments = models.ManyToManyField('user_auth.Departments', related_name='worker')
    course = models.ManyToManyField('user_auth.Course', related_name='worker')
    descriptions = models.CharField(max_length=500, blank=True, null=True)

    def __str__(self):
        return self.user.phone_number
