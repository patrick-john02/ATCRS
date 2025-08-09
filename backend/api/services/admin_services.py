from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User

#permissions 
from rest_framework.permissions import IsAuthenticated, AllowAny
#permissions
from api.permissions import(
    IsAdmin,
    IsSuperAdmin,
    IsApplicant,
)
#models
from api.models.admission import (
    Course,
)
from api.models.auth import ApplicantProfile
from api.models.exam import (
    Exam,
    Question,
    Choice,
    ApplicantExam,
    ApplicantAnswer,
    
)

#serializers
from api.serializers.AdmissionSerializer import (
    UserSerializers,
    CourseSerializers,
    ChoiceSerializer,
    QuestionSerializer,
    ExamSerializer,
    ApplicantExamSerializer,
    ApplicantAnswerSerializer,
    
)

from api.serializers.SuperAdminUserSerializer import(
    SuperAdminUserSerializer
)

class ChoiceView(viewsets.ModelViewSet):
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer
    permission_classes = [AllowAny]
    
class QuestionView(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [AllowAny]

class ExamView(viewsets.ModelViewSet):
    queryset = Exam.objects.all()
    serializer_class = ExamSerializer
    permission_classes = [AllowAny]

class ApplicantExamView(viewsets.ModelViewSet):
    queryset = ApplicantExam.objects.all()
    serializer_class = ApplicantExamSerializer
    permission_classes = [AllowAny]

class ApplicantAnswerView(viewsets.ModelViewSet):
    queryset = ApplicantAnswer.objects.all()
    serializer_class = ApplicantAnswerSerializer
    permission_classes = [AllowAny]    

class UsersView(viewsets.ModelViewSet):    
    queryset = ApplicantProfile.objects.all()
    serializer_class = UserSerializers
    permission_classes = [AllowAny]

class CoursesView(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializers
    permission_classes = [AllowAny]


#DASHBOARD
class AdminDashboardView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, requests, *args, **kwargs):
        exams_count = Exam.objects.all().count()
        applicants_count = ApplicantProfile.objects.filter(user_type = 'applicants').count()
        course_count = Course.objects.all().count()
        return Response({'applicants_count': applicants_count, 
                         'course_count': course_count,
                         'exams_count' : exams_count
                         })
