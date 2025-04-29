from django.contrib import admin

from user_auth.models import Teacher, User, Course, Departments, Group, Student, Table, Parents, GroupHomeWork, \
    TableType, HomeWork, Rooms, LessonAttendance, Worker,Lesson


admin.site.register([User,Teacher,Student,Parents,
                     Course,Departments,Group,GroupHomeWork,
                     Table,TableType,HomeWork,Rooms,LessonAttendance,Worker,Lesson])
