from .views import *
# from django.contrib import admin
from django.urls import path,include
from rest_framework.routers import  DefaultRouter

from .views.homework_view import AttendanceViewSet, TableViewSet, GroupViewSet, HomeWorkViewSet, GroupHomeWorkViewSet, \
    TopicsViewSet, TableTypeViewSet, CourseViewSet, ParentsViewSet, RoomsViewSet, DepartmentsViewSet
from .views.statistics_view import AttendanceStatisticsView, CourseStatisticsView, GroupStatisticsView, \
    PaymentsStatisticsView, StudentStatisticsView, TeacherStatisticsView
from .views.student_view import Student_Api
from .views.teacher_view import Crud_Teacher
from .views.worker_views import WorkerViewSet

router=DefaultRouter()

router.register('table', TableViewSet)
router.register('group', GroupViewSet)
router.register('homework', HomeWorkViewSet)
router.register('group_homework', GroupHomeWorkViewSet)
router.register('topics', TopicsViewSet)
router.register('worker', WorkerViewSet)
router.register('table_type', TableTypeViewSet)
router.register('course', CourseViewSet)
router.register('parents', ParentsViewSet)
router.register('rooms', RoomsViewSet)
router.register('departments', DepartmentsViewSet)

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [

    path("",include(router.urls)),
    path("get_phone/",PhoneSendOTP.as_view()),
    path("post_phone/",VerifySMS.as_view()),
    path('crud_teacher/',Crud_Teacher.as_view()),
    path('teacher_api/',Teacher_Api.as_view()),
    path('student_api/',Student_Api.as_view()),
    path('payments/',PaymentsApi.as_view()),
    path('attendance-statistics/', AttendanceStatisticsView.as_view(), name='attendance-statistics'),
    path('courses-statistics/', CourseStatisticsView.as_view(), name='courses-statistics'),
    path('groups-statistics/', GroupStatisticsView.as_view(), name='groups-statistics'),
    path('payments-statistics/', PaymentsStatisticsView.as_view(), name='payments-statistics'),
    path('students-statistic/', StudentStatisticsView.as_view(), name='students-statistics'),
    path('teachers-statistic/', TeacherStatisticsView.as_view(), name='teachers-statistics'),
    path('attendance/',AttendanceCreateAPIView.as_view()),
    path('teacher_attendance/',TeacherAttendanceCreateAPIView.as_view()),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path("loginApi/",LoginApi.as_view()),

]
