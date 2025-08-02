from rest_framework import viewsets
from django.contrib.auth.models import User

#permissions 
from rest_framework.permissions import IsAuthenticated, AllowAny
from api.permissions import(
    IsAdmin,
    IsSuperAdmin,
    IsApplicant,
)


#models
from api.models.admission import Course
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
    
