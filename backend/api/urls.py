from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from api.views import RegistrationView, CurrentUserView

#admin
from api.services.admin_services import (
    CoursesView,
    UsersView,
    ExamView,
    QuestionView,
    ChoiceView,
    ApplicantExamView,
    ApplicantAnswerView,
    AdminDashboardView,
    AdminApplicantsViewSet,
    AdminViewResultsViewSet,
    AdminPassedApplicantsViewSet,
    AdminFailedApplicantsViewSet,
    AdminCourseStatisticsView,
)
#super admin
from api.services.super_admin_services import (
    SuperAdminUserViewSet,
    SuperAdminApplicantsViewSet,
    SuperAdminManageCourses,
)
#applicants
from api.services.applicant_services import(
    UpcomingExamView,
    RecentExamScoresView,
    StartExamView,
    ApplicantProfileViewSet,
    ApplicantExamSummaryView,
    ApplicantExamHistoryView,
    TakeExamViewSet,
    

)
router = DefaultRouter()

router.register(r'register', RegistrationView, basename='registration') 

#admin side
router.register(r'admin-manage-courses', CoursesView, basename='admin-courses')
router.register(r'users', UsersView, basename='users')
router.register(r'applicants', AdminApplicantsViewSet, basename='applicants')

router.register(r'choices', ChoiceView, basename='choices')
router.register(r'questions', QuestionView, basename='questions')
router.register(r'exams', ExamView, basename='exams')
router.register(r'applicant-exam', ApplicantExamView, basename='applicant-exam')
router.register(r'applicant-answers', ApplicantAnswerView, basename='applicant-answers')

router.register(r'admin/results/passed', AdminPassedApplicantsViewSet, basename='admin-passed-applicants')
router.register(r'admin/results/failed', AdminFailedApplicantsViewSet, basename='admin-failed-applicants')
router.register(r'admin/results', AdminViewResultsViewSet, basename='admin-results')

#super admin side
router.register(r'superadmin/admin-users', SuperAdminUserViewSet, basename='superadmin-admin-users')
router.register(r'superadmin/applicants', SuperAdminApplicantsViewSet, basename='superadmin-applicants')
router.register(r'superadmin/manage-courses', SuperAdminManageCourses, basename='superadmin-courses')

# applicants side
router.register(r'upcoming-exams', UpcomingExamView, basename='upcoming-exams')
router.register(r'recent-exam-scores', RecentExamScoresView, basename='recent-exam-scores')
router.register(r'start-exam', StartExamView, basename='start-exam')
router.register(r'profile', ApplicantProfileViewSet, basename='applicant-profile')
router.register(r'exam-summary', ApplicantExamSummaryView, basename='exam-summary')

router.register(r'exam-history', ApplicantExamHistoryView, basename='exam-history')
router.register(r'take-exam', TakeExamViewSet, basename='take-exam')




urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('users/me/', CurrentUserView.as_view(), name='user-detail'),
    
    #admin
    path('admin-dashboard/', AdminDashboardView.as_view(), name = 'dashboard_admin_count'),
    path('admin/course-statistics/', AdminCourseStatisticsView.as_view(), name='admin-course-statistics'),
    
    path('', include(router.urls)),
]