from .views import *
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views.lesson_view import LessonCreateWithAttendance, LessonWithAttendanceGet, UpdateLessonView, DeleteLessonView, \
    AttendanceUpdateView, \
    AllLessonList

from .views.student_view import Student_Api, StudentDetail
from .views.teacher_view import Teacher_Api, TeacherDetail
from .views.user_crud_view import StaffCreate, UserApi, UserDetail

router = DefaultRouter()

router.register('table', TableViewSet)
router.register('group', GroupViewSet)
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
    path('auth_user/create/staff/', StaffCreate.as_view()),
    path('auth_user/login/', LoginApi.as_view()),
    path('auth_user/auth_me/', AuthMeView.as_view()),
    path('auth_user/set_password', SetPasswordView.as_view()),
    path('auth_user/create/user/', RegisterUserApi.as_view()),
    path('auth_user/change_password/', ChangePasswordView.as_view()),
    path('auth_user/phone_send_otp/', PhoneSendOTP.as_view()),
    path('auth_user/verify_sms/', ResetPassword.as_view()),
    path('auth_user/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth_user/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth_user/logout/', LogoutView.as_view()),

    # User CRUD
    path('user/api/', UserApi.as_view()),
    path('user/detail/<int:pk>/', UserDetail.as_view()),

    # Teacher CRUD
    path('teacher_api/', Teacher_Api.as_view()),
    path('teacher_api/<int:pk>/', TeacherDetail.as_view()),
    path('teacher_api/get_group_students/', TeacherGetGroupStudents.as_view()),
    path('teacher_api/get_groups/', TeacherGetGroups.as_view()),
    path('teacher_api/get_homeworks/', TeacherGetHomeworkStatistic.as_view()),
    path('teacher_api/get_attendance/', TeacherGetAttendanceStatistic.as_view()),
    path('teacher_api/teacher_update_group_title/<int:pk>/', TeacherUpdateGroupTitle.as_view()),

    # Student CRUD
    path('student_api/', Student_Api.as_view()),
    path('student_api/<int:pk>/', StudentDetail.as_view()),
    path('student_api/student_get_homework/', StudentGetHomeworks.as_view()),
    path('student_api/student_get_attendance/', StudentGetAttendance.as_view()),
    path('student_api/student_get_payments/', StudentGetPayments.as_view()),

    # Payment
    path('payment/create/month/', MonthApi.as_view()),
    path('payment/create/month/detail/<int:pk>/', MonthDetail.as_view()),
    path('payment/create/payment_type/', PaymentTypeApi.as_view()),
    path('payment/detail/payment_type/<int:pk>/', PaymentTypeDetail.as_view()),
    path('payment/create/payment/', PaymentApi.as_view()),
    path('payment/create/payment/detail/<int:pk>/', PaymentDetail.as_view()),

    # Lesson
    path('lesson/lesson_attendance_create/', LessonCreateWithAttendance.as_view()),
    path('lesson/all_lesson_list/', AllLessonList.as_view()),
    path('lesson/lesson_attendance_full_update/<int:pk>/', LessonFullUpdateView.as_view()),
    path('lesson/lesson_attendance_get/<int:pk>/', LessonWithAttendanceGet.as_view()),
    path('lesson/<int:pk>/update/', UpdateLessonView.as_view()),
    path('lesson/lesson_delete/<int:pk>/', DeleteLessonView.as_view()),
    path('lesson/only_attendance_update/<int:pk>/', AttendanceUpdateView.as_view()),

    # Homework
    path('homework/group_homework_api/', GroupHomeWorkAPIView.as_view()),
    path('homework/group_homework_detail/<int:pk>/', GroupHomeWorkDetailView.as_view()),
    path('homework/homework_api/', HomeWorkAPIView.as_view()),
    path('homework/homework_detail/<int:pk>/', HomeWorkDetailView.as_view()),
    path('homework/homework_review_api/', HomeworkReviewAPIView.as_view()),
    path('homework/homework_review_detail/<int:pk>/', HomeworkReviewDetailView.as_view()),

    # Statistics data
    path('statistics/students/', StudentsStatisticsView.as_view()),
    path('statistics/payments/', PaymentStatisticsView.as_view()),
    path('statistics/lesson_attendance/<int:pk>/', LessonAttendanceStatisticsView.as_view()),

    # Test Funksiya
    # path('test/salom/',SalomBer.as_view())

]
