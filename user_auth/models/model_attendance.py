from django.db import models

# class Attendance(models.Model):
#     group = models.ForeignKey('user_auth.Group', on_delete=models.CASCADE)
#     date = models.DateField()
#     descriptions = models.TextField(blank=True)
#
#     def __str__(self):
#         return f"{self.group.title} - {self.date}"
#
# class StudentAttendance(models.Model):
#     STATUS_CHOICES = [
#         ('bor', "Bor"),
#         ("yo'q", "Yo'q"),
#         ("kechikkan", "Kechikkan"),
#         ("sababli","Sabali")
#     ]
#     attendance = models.ForeignKey(Attendance, on_delete=models.CASCADE, related_name='student_attendances')
#     student = models.ForeignKey('user_auth.Student', on_delete=models.CASCADE)
#     status = models.CharField(max_length=10, choices=STATUS_CHOICES)
#
# class TeacherAttendance(models.Model):
#     STATUS_CHOICES = [
#         ('bor', "Bor"),
#         ("yo'q", "Yo'q"),
#         ("kechikkan", "Kechikkan"),
#         ("sababli", "Sabali")
#     ]
#     attendance = models.ForeignKey(Attendance, on_delete=models.CASCADE, related_name='teacher_attendances')
#     teacher = models.ForeignKey('user_auth.Teacher', on_delete=models.CASCADE)
#     status = models.CharField(max_length=10, choices=STATUS_CHOICES)

class Attendance(models.Model):
    STATUS_CHOICES = (
        ('keldi', 'Keldi'),
        ('kelmadi', 'Kelmadi'),
        ('kechikkan', 'Kechikkan'),
        ('sababli', 'Sababli'),
    )
    group = models.ForeignKey('user_auth.Group', on_delete=models.CASCADE, related_name='attendances')
    student = models.ForeignKey('user_auth.Student', on_delete=models.CASCADE, related_name='attendances')
    date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)

    def __str__(self):
        return f"{self.student.user.phone_number} - {self.date} - {self.status}"