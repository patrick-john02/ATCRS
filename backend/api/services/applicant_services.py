from rest_framework import viewsets
from rest_framework.decorators import action
from django.db.models import Count, F
from rest_framework import status
from rest_framework.permissions import IsAuthenticated , AllowAny
from rest_framework.response import Response
from django.utils import timezone
from api.models.exam import Exam, ApplicantExam
from api.permissions import IsApplicant
from api.serializers.AdmissionSerializer import (
    UpcomingExamSerializer,
    RecentApplicantExamSerializer
)
from api.serializers.ApplicantsSerializer import (
    StartExamSerializer,
    ApplicantProfileSerializer,
    ApplicantExamSummarySerializer,
    ApplyUpcomingExamSerializer,
    ApplicantExamHistorySerializer,
    TakeExamSerializer,
    SubmitAnswerSerializer,
    CompleteExamSerializer,
    
)

from api.models.auth import ApplicantProfile

class UpcomingExamView(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated, IsApplicant]
    serializer_class = UpcomingExamSerializer
    lookup_field = 'uuid'

    def get_queryset(self):
        today = timezone.now().date()
        return Exam.objects.filter(
            is_active=True,
            is_expired=False,
            date__gte=today
        ).annotate(
            applicant_count=Count('applicantexam')
        ).filter(applicant_count__lt=F('max_applicants')).order_by('date')
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    @action(detail=True, methods=['post'], serializer_class=ApplyUpcomingExamSerializer)
    def apply(self, request, uuid=None):
        exam = self.get_object()
        serializer = ApplyUpcomingExamSerializer(
            data={'exam_uuid': str(exam.uuid)}, 
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        applicant_exam = serializer.save()
        return Response({
            'message': 'Successfully applied to exam',
            'data': ApplyUpcomingExamSerializer(applicant_exam).data
        }, status=201)

    
class RecentExamScoresView(viewsets.ReadOnlyModelViewSet):
    serializer_class = RecentApplicantExamSerializer
    permission_classes = [IsAuthenticated, IsApplicant]

    def get_queryset(self):
        user = self.request.user
        try:
            applicant = user.applicantprofile
        except:
            return ApplicantExam.objects.none()

        return ApplicantExam.objects.filter(applicant=applicant).order_by('-created_at')[:5]


#start exam
class StartExamView(viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated, IsApplicant]
    serializer_class = StartExamSerializer
    

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        from django.db import transaction

        with transaction.atomic():
            applicant_exam = serializer.save(applicant=request.user.applicantprofile)

        return Response(self.get_serializer(applicant_exam).data, status=status.HTTP_201_CREATED)

#profile
class ApplicantProfileViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsApplicant]
    serializer_class = ApplicantProfileSerializer

    def get_queryset(self):
        user = self.request.user
        return ApplicantProfile.objects.filter(user=user)
    

#exam summarry
class ApplicantExamSummaryView(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated, IsApplicant]
    serializer_class = ApplicantExamSummarySerializer

    def get_queryset(self):
        user = self.request.user
        try:
            applicant = user.profile 
        except ApplicantProfile.DoesNotExist:
            return ApplicantExam.objects.none()
        return ApplicantExam.objects.filter(applicant=applicant).order_by('-created_at')
    
class ApplicantExamHistoryView(viewsets.ReadOnlyModelViewSet):
    serializer_class = ApplicantExamHistorySerializer
    permission_classes = [IsAuthenticated, IsApplicant]
    #permission_classes = [AllowAny]
    lookup_field = 'uuid'
    
    def get_queryset(self):
        user = self.request.user
        try:
            applicant = user.profile
        except:
            return ApplicantExam.objects.none()
        
        return ApplicantExam.objects.filter(
            applicant=applicant
        ).select_related('exam', 'recommended_course').order_by('-created_at')

class TakeExamViewSet(viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated, IsApplicant]
    serializer_class = TakeExamSerializer
    lookup_field = 'uuid'
    
    def get_queryset(self):
        user = self.request.user
        try:
            applicant = user.profile
        except:
            return ApplicantExam.objects.none()
        
        return ApplicantExam.objects.filter(
            applicant=applicant,
            status__in=['not_started', 'in_progress']
        ).select_related('exam')
    
    def retrieve(self, request, uuid=None):
        """Get exam details and questions"""
        try:
            applicant_exam = self.get_queryset().get(uuid=uuid)
            
            # Start exam if not started
            if applicant_exam.status == 'not_started':
                applicant_exam.status = 'in_progress'
                applicant_exam.started_at = timezone.now()
                applicant_exam.save()
            
            serializer = self.get_serializer(applicant_exam)
            return Response(serializer.data)
        except ApplicantExam.DoesNotExist:
            return Response(
                {'error': 'Exam not found or already completed'},
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=True, methods=['post'], serializer_class=SubmitAnswerSerializer)
    def submit_answer(self, request, uuid=None):
        """Submit answer for a question"""
        applicant_exam = self.get_object()
        
        if applicant_exam.status != 'in_progress':
            return Response(
                {'error': 'Exam is not in progress'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = SubmitAnswerSerializer(
            data=request.data,
            context={'applicant_exam': applicant_exam}
        )
        serializer.is_valid(raise_exception=True)
        answer = serializer.save()
        
        return Response({
            'message': 'Answer submitted successfully',
            'is_correct': answer.is_correct,
            'attempted_questions': applicant_exam.attempted_questions,
            'total_questions': applicant_exam.total_questions,
        }, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['post'], serializer_class=CompleteExamSerializer)
    def complete(self, request, uuid=None):
        """Complete and submit the exam"""
        applicant_exam = self.get_object()
        
        if applicant_exam.status != 'in_progress':
            return Response(
                {'error': 'Exam is not in progress'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = CompleteExamSerializer(
            context={'applicant_exam': applicant_exam}
        )
        completed_exam = serializer.save()
        
        return Response({
            'message': 'Exam completed successfully',
            'score': completed_exam.recommendation_score,
            'correct_answers': completed_exam.correct_answers,
            'total_questions': completed_exam.total_questions,
            'recommended_course': completed_exam.recommended_course.name if completed_exam.recommended_course else None,
        }, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['get'])
    def progress(self, request, uuid=None):
        """Get current exam progress"""
        applicant_exam = self.get_object()
        
        return Response({
            'attempted_questions': applicant_exam.attempted_questions,
            'total_questions': applicant_exam.total_questions,
            'time_started': applicant_exam.started_at,
            'duration_minutes': applicant_exam.exam.duration_minutes,
        })