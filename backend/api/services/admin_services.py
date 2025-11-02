from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework.decorators import action

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
    AdminResultSerializer,
    
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
    permission_classes = [AllowAny]
    lookup_field = "uuid"
    
class QuestionView(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [AllowAny]
    lookup_field = "uuid"

    @action(detail=True, methods=["post"], url_path="choices")
    def create_choice(self, request, uuid=None):
        question = self.get_object()
        serializer = ChoiceSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(question=question)
        return Response(serializer.data)

class ExamView(viewsets.ModelViewSet):
    queryset = Exam.objects.all()
    serializer_class = ExamSerializer
    permission_classes = [AllowAny]
    lookup_field = "uuid"

    @action(detail=True, methods=["post"], url_path="questions")
    def create_question(self, request, uuid=None):
        exam = self.get_object()
        serializer = QuestionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(exam=exam)
        return Response(serializer.data)

class ApplicantExamView(viewsets.ModelViewSet):
    queryset = ApplicantExam.objects.all()
    serializer_class = ApplicantExamSerializer
    permission_classes = [IsAdmin, IsAuthenticated]
    lookup_field = 'uuid'

class ApplicantAnswerView(viewsets.ModelViewSet):
    queryset = ApplicantAnswer.objects.all()
    serializer_class = ApplicantAnswerSerializer
    permission_classes = [IsAdmin, IsAuthenticated] 
    lookup_field = 'uuid' 

class UsersView(viewsets.ModelViewSet):    
    queryset = ApplicantProfile.objects.all()
    serializer_class = UserSerializers
    permission_classes = [IsAdmin, IsAuthenticated]

class CoursesView(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializers
    permission_classes = [IsAdmin, IsAuthenticated]
    lookup_field = 'uuid'


#DASHBOARD
class AdminDashboardView(APIView):
    permission_classes = [IsAdmin, IsAuthenticated]
    
    def get(self, requests, *args, **kwargs):
        exams_count = Exam.objects.all().count()
        applicants_count = ApplicantProfile.objects.filter(user_type = 'applicant').count()
        course_count = Course.objects.all().count()
        return Response({'applicants_count': applicants_count, 
                         'course_count': course_count,
                         'exams_count' : exams_count
                         })

class AdminCourseStatisticsView(APIView):
    permission_classes = [IsAdmin, IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        from django.db.models import Count, Q
        
        courses = Course.objects.annotate(
            total_applicants=Count(
                'applicantprofile',
                filter=Q(applicantprofile__user_type='applicant'),
                distinct=True
            ),
            recommended_count=Count(
                'recommended_exams',
                filter=Q(recommended_exams__status='completed'),
                distinct=True
            )
        ).values('name', 'total_applicants', 'recommended_count')
        
        return Response(list(courses))


#results
class AdminViewResultsViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = AdminResultSerializer  # Changed
    permission_classes = [IsAdmin, IsAuthenticated]
    lookup_field = 'uuid'
    
    def get_queryset(self):
        queryset = ApplicantExam.objects.filter(status='completed').select_related(
            'applicant__user',
            'exam',
            'recommended_course'
        ).order_by('-completed_at')
        
        exam_uuid = self.request.query_params.get('exam')
        if exam_uuid:
            queryset = queryset.filter(exam__uuid=exam_uuid)
        
        course_id = self.request.query_params.get('course')
        if course_id:
            queryset = queryset.filter(recommended_course_id=course_id)
            
        return queryset
    
    
class AdminPassedApplicantsViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = AdminResultSerializer
    permission_classes = [IsAdmin, IsAuthenticated]
    lookup_field = 'uuid'
    
    def get_queryset(self):
        queryset = ApplicantExam.objects.filter(
            status='completed',
            recommended_course__isnull=False
        ).select_related(
            'applicant__user',
            'exam',
            'recommended_course'
        ).order_by('-recommendation_score', '-completed_at')
        
        # Optional filters
        min_score = self.request.query_params.get('min_score')
        if min_score:
            queryset = queryset.filter(recommendation_score__gte=min_score)
        
        course_id = self.request.query_params.get('course')
        if course_id:
            queryset = queryset.filter(recommended_course_id=course_id)
            
        return queryset
    

class AdminFailedApplicantsViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = AdminResultSerializer
    permission_classes = [IsAdmin, IsAuthenticated]
    lookup_field = 'uuid'
    
    def get_queryset(self):
        queryset = ApplicantExam.objects.filter(
            status='completed',
            recommended_course__isnull=True
        ).select_related(
            'applicant__user',
            'exam',
            'recommended_course'
        ).order_by('-completed_at')
        
        # Optional filters
        max_score = self.request.query_params.get('max_score')
        if max_score:
            queryset = queryset.filter(recommendation_score__lte=max_score)
        
        exam_uuid = self.request.query_params.get('exam')
        if exam_uuid:
            queryset = queryset.filter(exam__uuid=exam_uuid)
            
        return queryset