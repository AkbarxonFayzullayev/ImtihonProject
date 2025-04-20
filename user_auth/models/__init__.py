from .auth_users import BaseModel,CustomUserManager,User
from .model_group import Group,Course
from .model_table import Table,TableType,Rooms
from .model_homework import Topics,GroupHomeWork,HomeWork
from .model_student import Student,Parents
from .model_teacher import Teacher,Departments
from .model_attendance import Attendance,StudentAttendance
from .model_worker import Worker

__all__ = [
    "User", "BaseModel",
    "Group", "Course",
    "Table",
    "GroupHomeWork", "HomeWork",
    "Student", "Parents",
    "Teacher",
    "Attendance",
    "Worker",
    "StudentAttendance"
]
