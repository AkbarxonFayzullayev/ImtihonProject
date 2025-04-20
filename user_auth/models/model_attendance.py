from django.db import models
#
#
# class Attendance(models.Model):
#     STATUS_CHOICES = (
#         ('bor', 'Bor'),
#         ("yo'q", "Yo'q"),
#         ('kechikkan', 'Kechikkan'),
#     )
#     group = models.ForeignKey('user_auth.Group', on_delete=models.RESTRICT)
#     student = models.ForeignKey('user_auth.Student', on_delete=models.RESTRICT,default=1)
#     date = models.DateField()
#     status = models.CharField(max_length=10,choices=STATUS_CHOICES,default='absent')
#     descriptions = models.CharField(max_length=400,null=True,blank=True)
#
#     def __str__(self):
#         return f"{self.student.phone_number} - {self.date} - {self.status}"
class Attendance(models.Model):
    group = models.ForeignKey('user_auth.Group', on_delete=models.CASCADE)
    date = models.DateField()
    descriptions = models.TextField(blank=True)

    def __str__(self):
        return f"{self.group.name} - {self.date}"

class StudentAttendance(models.Model):
    STATUS_CHOICES = [
        ('bor', "Bor"),
        ("yo'q", "Yo'q"),
        ("kechikkan", "Kechikkan"),
    ]
    attendance = models.ForeignKey(Attendance, on_delete=models.CASCADE, related_name='student_attendances')
    student = models.ForeignKey('user_auth.Student', on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)