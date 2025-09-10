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

class AdminApplicantsViewSet(viewsets.ModelViewSet):
    serializer_class = SuperAdminUserSerializer
    permission_classes = [IsAdmin, IsAuthenticated]
    
    def get_queryset(self):
        queryset = ApplicantProfile.objects.filter(user_type = 'applicant').order_by('created_at')
        
        is_verified_param = self.request.query_params.get('is_verified')
        if is_verified_param is not None:
            if is_verified_param.lower() == 'true':
                queryset = queryset.filter(is_verified=True)
            if is_verified_param.lower() == 'false':
                queryset = queryset.filter(is_verified = False)
        return queryset

#manage exams
class ChoiceView(viewsets.ModelViewSet):
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer
    permission_classes = [IsAdmin, IsAuthenticated]
    
class QuestionView(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [AllowAny]

class ExamView(viewsets.ModelViewSet):
    queryset = Exam.objects.all()
    serializer_class = ExamSerializer
    permission_classes = [AllowAny]
    lookup_field = 'uuid'

class ApplicantExamView(viewsets.ModelViewSet):
    queryset = ApplicantExam.objects.all()
    serializer_class = ApplicantExamSerializer
    permission_classes = [IsAdmin, IsAuthenticated]

class ApplicantAnswerView(viewsets.ModelViewSet):
    queryset = ApplicantAnswer.objects.all()
    serializer_class = ApplicantAnswerSerializer
    permission_classes = [IsAdmin, IsAuthenticated]   

class UsersView(viewsets.ModelViewSet):    
    queryset = ApplicantProfile.objects.all()
    serializer_class = UserSerializers
    permission_classes = [IsAdmin, IsAuthenticated]

class CoursesView(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializers
    permission_classes = [IsAdmin, IsAuthenticated]


#DASHBOARD
class AdminDashboardView(APIView):
    permission_classes = [IsAdmin, IsAuthenticated]
    
    def get(self, requests, *args, **kwargs):
        exams_count = Exam.objects.all().count()
        applicants_count = ApplicantProfile.objects.filter(user_type = 'applicants').count()
        course_count = Course.objects.all().count()
        return Response({'applicants_count': applicants_count, 
                         'course_count': course_count,
                         'exams_count' : exams_count
                         })
