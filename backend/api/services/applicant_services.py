from rest_framework import viewsets
from rest_framework.decorators import action
from django.db.models import Count, F
from rest_framework.permissions import IsAuthenticated
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
    
)

from api.models.auth import ApplicantProfile

class UpcomingExamView(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated, IsApplicant]
    serializer_class = UpcomingExamSerializer
    lookup_field = 'uuid'  # <--- add this

    def get_queryset(self):
        today = timezone.now().date()
        return Exam.objects.filter(
            is_active=True,
            is_expired=False,
            date__gte=today
        ).annotate(
            applicant_count=Count('applicantexam')
        ).filter(applicant_count__lt=F('max_applicants')).order_by('date')

    @action(detail=True, methods=['post'], serializer_class=ApplyUpcomingExamSerializer)
    def apply(self, request, uuid=None):  # <- change pk to uuid
        exam = self.get_object()
        serializer = ApplyUpcomingExamSerializer(
            data={'exam_id': exam.id}, 
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        applicant_exam = serializer.save()
        return Response(ApplyUpcomingExamSerializer(applicant_exam).data, status=201)


    
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