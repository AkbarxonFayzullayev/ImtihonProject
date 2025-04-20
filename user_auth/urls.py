from .views import *
# from django.contrib import admin
from django.urls import path,include
from rest_framework.routers import  DefaultRouter

from .views.homework_view import AttendanceViewSet, TableViewSet, GroupViewSet, HomeWorkViewSet, GroupHomeWorkViewSet, \
    TopicsViewSet, TableTypeViewSet, CourseViewSet, ParentsViewSet, RoomsViewSet, DepartmentsViewSet
from .views.student_view import Student_Api
from .views.teacher_view import Crud_Teacher
from .views.worker_views import WorkerViewSet

router=DefaultRouter()
# router.register('attendance', AttendanceViewSet)
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
# router.register('payments', PaymentsViewSet)

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
    path('attendance/',AttendanceCreateAPIView.as_view()),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path("loginApi/",LoginApi.as_view()),

]
