from datetime import date

from django.db import models


class Lesson(models.Model):
    title = models.CharField(max_length=100)
    group = models.ForeignKey('user_auth.Group',on_delete=models.CASCADE,default=1)
    date = models.DateField(default=date.today)
    table = models.ForeignKey('user_auth.Table',on_delete=models.CASCADE,default=1)
    descriptions = models.CharField(max_length=400,blank=True,null=True,default="Tavsif yo'q")

    def __str__(self):
        return self.title


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

class GroupHomeWork(models.Model):
    group = models.ForeignKey('user_auth.Group', on_delete=models.CASCADE)
    title = models.CharField(max_length=200,default="Noma'lum title")
    lesson = models.ForeignKey('user_auth.Lesson', on_delete=models.CASCADE,null=True,blank=True)
    file = models.FileField(upload_to='homeworks/', blank=True, null=True)
    deadline = models.DateField(default=date.today)
    descriptions = models.CharField(max_length=400, blank=True, null=True)

    def __str__(self):
        return self.lesson.title

class HomeWork(models.Model):
    group_homework = models.ForeignKey('user_auth.GroupHomeWork', on_delete=models.CASCADE)
    student = models.ForeignKey('user_auth.Student', on_delete=models.CASCADE)
    link = models.URLField(blank=True,null=True)
    descriptions = models.CharField(max_length=500,default="uyga vazifa bajarildi.")
    is_checked = models.BooleanField(default=False)

    def __str__(self):
        if self.link:
            return self.link
        return f"{self.student.user.phone_number} uchun homework"

class HomeworkReview(models.Model):
    homework = models.OneToOneField('user_auth.HomeWork',on_delete=models.CASCADE)
    score = models.IntegerField()
    comment = models.TextField()
