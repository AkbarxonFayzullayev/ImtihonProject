from django.db import models
from .auth_users import BaseModel


class Student(BaseModel):
    user = models.OneToOneField('user_auth.User', on_delete=models.CASCADE,related_name='student')
    fullname = models.CharField(max_length=50,default='Unknown Student')
    course = models.ManyToManyField('user_auth.Course',related_name="get_student_course")
    group = models.ManyToManyField('user_auth.Group', related_name='students')
    is_line = models.BooleanField(default=True)
    descriptions = models.CharField(max_length=500, blank=True, null=True)

    def __str__(self):
        return self.user.phone_number

class Parents(BaseModel):
    student = models.OneToOneField('user_auth.Student', on_delete=models.CASCADE, related_name='get_student')
    full_name = models.CharField(max_length=50, null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    descriptions = models.CharField(max_length=500, null=True, blank=True)
    def __str__(self):
        return self.full_name
