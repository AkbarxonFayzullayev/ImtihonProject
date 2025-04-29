from .auth_users import BaseModel,CustomUserManager,User
from .model_group import Group,Course
from .model_table import Table,TableType,Rooms
from .model_lesson import Lesson, GroupHomeWork, HomeWork, LessonAttendance
from .model_student import Student,Parents
from .model_teacher import Teacher,Departments
from .model_worker import Worker

__all__ = [
    "User", "BaseModel",
    "Group", "Course",
    "Table","TableType",
    "GroupHomeWork", "HomeWork",
    "Student", "Parents",
    "Teacher",
    "LessonAttendance",
    "Worker",
    "Lesson",
    # "StudentAttendance",
    "Rooms","Departments"
]
