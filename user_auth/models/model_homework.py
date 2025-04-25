from django.db import models

class Lesson(models.Model):
    title = models.CharField(max_length=100)
    course = models.ForeignKey('user_auth.Course',on_delete=models.RESTRICT)
    is_active = models.BooleanField(default=True)
    descriptions = models.CharField(max_length=400,blank=True,null=True,default="Tavsif yo'q")

    def __str__(self):
        return self.title

class GroupHomeWork(models.Model):
    group = models.ForeignKey('user_auth.Group', on_delete=models.RESTRICT)
    lesson = models.ForeignKey('user_auth.Lesson', on_delete=models.RESTRICT)
    is_active = models.BooleanField(default=True)
    descriptions = models.CharField(max_length=400, blank=True, null=True)

    def __str__(self):
        return self.lesson.title

class HomeWork(models.Model):
    groupHomeWork = models.ForeignKey('user_auth.GroupHomeWork', on_delete=models.RESTRICT)
    score = models.CharField(max_length=5, null=True, blank=True)
    student = models.ForeignKey('user_auth.Student', on_delete=models.RESTRICT)
    link = models.URLField()
    is_active = models.BooleanField(default=False)
    descriptions = models.CharField(max_length=500, blank=True, null=True)

    def __str__(self):
        return self.link
