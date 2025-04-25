from .views import *
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views.homework_view import  TableViewSet, GroupViewSet, HomeWorkViewSet, GroupHomeWorkViewSet, \
    TopicsViewSet, TableTypeViewSet, CourseViewSet, ParentsViewSet, RoomsViewSet, DepartmentsViewSet
from .views.mock_data import Mock_data
from .views.statistics_view import AttendanceStatisticsView, CourseStatisticsView, GroupStatisticsView, \
    PaymentsStatisticsView, StudentStatisticsView, TeacherStatisticsView
from .views.student_view import Student_Api,StudentDetail
from .views.teacher_view import Teacher_Api,TeacherDetail
from .views.user_crud_view import AdminCreate, UserApi, UserDetail
from .views.worker_views import WorkerViewSet

router = DefaultRouter()

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

    path("", include(router.urls)),

    # Auth
    path('auth_user/create/admin/', AdminCreate.as_view()),
    path('auth_user/login/', LoginApi.as_view()),
    path('auth_user/auth_me', AuthMeView.as_view()),
    path('auth_user/set_password', SetPasswordView.as_view()),
    path('auth_user/create/user/', RegisterUserApi.as_view()),
    path('auth_user/change_password/', ChangePasswordView.as_view()),
    path('auth_user/phone_send_otp/', PhoneSendOTP.as_view()),
    path('auth_user/verify_sms/', VerifySMS.as_view()),
    path('auth_user/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth_user/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth_user/logout/', LogoutView.as_view()),

    # User CRUD
    path('user/api/',UserApi.as_view()),
    path('user/detail/<int:pk>',UserDetail.as_view()),

    # Teacher and Student CRUD
    path('teacher_api/', Teacher_Api.as_view()),
    path('teacher_api/<int:pk>', TeacherDetail.as_view()),
    path('student_api/', Student_Api.as_view()),
    path('student_api/<int:pk>', StudentDetail.as_view()),

    # Payment
    path('payment/create/month/',MonthApi.as_view()),
    path('payment/create/month/detail/<int:pk>',MonthDetail.as_view()),
    path('payment/create/payment_type',PaymentTypeApi.as_view()),
    path('payment/detail/payment_type/<int:pk>',PaymentTypeDetail.as_view()),
    path('payment/create/payment', PaymentApi.as_view()),
    path('payment/create/payment/detail/<int:pk>', PaymentDetail.as_view()),

    # Statistics
    path('statistics/attendance/', AttendanceStatisticsView.as_view()),
    path('statistics/courses/', CourseStatisticsView.as_view()),
    path('statistics/groups/', GroupStatisticsView.as_view()),
    path('statistics/payments/', PaymentsStatisticsView.as_view()),
    path('statistics/students/', StudentStatisticsView.as_view()),
    path('statistics/teachers/', TeacherStatisticsView.as_view()),

    # Attendance
    path('attendance/request_user_student/',StudentRequestAttendanceView.as_view()),
    path('attendance/student/detail/<int:pk>',AttendanceUpdateAPIView.as_view()),
    path('attendance/all_attendances_get/',AllAttendanceList.as_view()),
    path('attendance/student/', AttendanceCreateAPIView.as_view()),
    path('attendance/student_attendance/<int:id>', StudentAttendanceView.as_view()),
    path('attendance/teacher/', TeacherAttendanceCreateAPIView.as_view()),

    # Mock data
    path('mock_data/',Mock_data.as_view())

]
