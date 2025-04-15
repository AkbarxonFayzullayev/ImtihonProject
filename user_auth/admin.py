from django.contrib import admin

from user_auth.models import Teacher, User, Course, Departments, GroupStudent, Student, Table

admin.site.register([User,Teacher,Student,Course,Departments,GroupStudent,Table])

