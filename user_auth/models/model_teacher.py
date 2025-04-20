from django.db import models

from user_auth.models import BaseModel


# Xodimlarning darajasini belgilash uchun
class Departments(BaseModel):
    title = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    descriptions = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.title


# Xodimlarning datalarini saqlash uchun yuqoridagi Course va Departments modellari Worker bog'langan
class Teacher(BaseModel):
    user = models.OneToOneField('user_auth.User', on_delete=models.CASCADE, related_name='user')
    departments = models.ManyToManyField('user_auth.Departments', related_name="get_department")
    course = models.ManyToManyField('user_auth.Course', related_name="get_teacher_course")
    descriptions = models.CharField(max_length=500, blank=True, null=True)

    def __str__(self):
        return f"{self.user.phone_number}"
