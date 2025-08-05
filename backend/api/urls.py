from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from api.views import RegistrationView, CurrentUserView
from api.services.admin_services import (
    CoursesView,
    UsersView,
    ExamView,
    QuestionView,
    ChoiceView,
    ApplicantExamView,
    ApplicantAnswerView,
)

from api.services.super_admin_services import (
    AdminUserViewSet
)
router = DefaultRouter()

router.register(r'register', RegistrationView, basename='registration') 

#admin side
router.register(r'courses', CoursesView, basename='courses')
router.register(r'users', UsersView, basename='users')

router.register(r'choices', ChoiceView, basename='choices')
router.register(r'questions', QuestionView, basename='questions')
router.register(r'exams', ExamView, basename='exams')
router.register(r'applicant-exam', ApplicantExamView, basename='applicant-exam')
router.register(r'applicant-answers', ApplicantAnswerView, basename='applicant-answers')

#super admin side
router.register(r'admin-users', AdminUserViewSet, basename='admin-users')


#applicants side
# router.register(r'admin-users', AdminUserViewSet, basename='admin-users')


urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('users/me/', CurrentUserView.as_view(), name='user-detail'),
    
    path('', include(router.urls)),
]