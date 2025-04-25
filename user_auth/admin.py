from django.contrib import admin

from user_auth.models import Teacher, User, Course, Departments, Group, Student, Table, Parents, GroupHomeWork, \
    TableType, HomeWork, Rooms, Attendance, Worker, StudentAttendance
from user_auth.models.model_attendance import TeacherAttendance

admin.site.register([User,StudentAttendance,TeacherAttendance,Teacher,Student,Parents,
                     Course,Departments,Group,GroupHomeWork,
                     Table,TableType,HomeWork,Rooms,Attendance,Worker])
