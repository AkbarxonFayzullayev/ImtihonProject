from django.db import models
from django.utils import timezone


class Lesson(models.Model):
    title = models.CharField(max_length=100)
    group = models.ForeignKey('user_auth.Group',on_delete=models.CASCADE,default=1)
    date = models.DateField(default=timezone.now)
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    descriptions = models.CharField(max_length=400,blank=True,null=True,default="Tavsif yo'q")

    def __str__(self):
        return self.title

class GroupHomeWork(models.Model):
    group = models.ForeignKey('user_auth.Group', on_delete=models.RESTRICT)
    lesson = models.ForeignKey('user_auth.Lesson', on_delete=models.RESTRICT,null=True,blank=True)
    file = models.FileField(upload_to='homeworks/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    descriptions = models.CharField(max_length=400, blank=True, null=True)

    def __str__(self):
        return self.lesson.title

class HomeWork(models.Model):
    groupHomeWork = models.ForeignKey('user_auth.GroupHomeWork', on_delete=models.RESTRICT)
    score = models.CharField(max_length=5, null=True, blank=True)
    student = models.ForeignKey('user_auth.Student', on_delete=models.RESTRICT)
    link = models.URLField(blank=True,null=True)
    is_active = models.BooleanField(default=True)
    descriptions = models.CharField(max_length=500, blank=True, null=True)

    def __str__(self):
        if self.link:
            return self.link
        return f"{self.student.user.phone_number} uchun homework"

class LessonAttendance(models.Model):
    STATUS_CHOICES = (
        ('keldi', 'Keldi'),
        ('kelmadi', 'Kelmadi'),
        ('kechikkan', 'Kechikkan'),
        ('sababli', 'Sababli'),
    )
    lesson = models.ForeignKey('user_auth.Lesson', on_delete=models.CASCADE, related_name='attendances')
    student = models.ForeignKey('user_auth.Student', on_delete=models.CASCADE, related_name='lesson_attendances')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)

    def __str__(self):
        return f"{self.student.user.phone_number} - {self.lesson.date} - {self.status}"
