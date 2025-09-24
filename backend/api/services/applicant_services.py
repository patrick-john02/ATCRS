from rest_framework import viewsets
from django.db.models import Count, F
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.utils import timezone
from api.models.exam import Exam, ApplicantExam
from api.serializers.AdmissionSerializer import (
    UpcomingExamSerializer,
    RecentApplicantExamSerializer
)
from api.serializers.ApplicantsSerializer import (
    StartExamSerializer,
    
)

class UpcomingExamView(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = UpcomingExamSerializer

    def get_queryset(self):
        today = timezone.now().date()
        return Exam.objects.filter(
            is_active=True,
            is_expired=False,
            date__gte=today
        ).annotate(
            applicant_count=Count('applicantexam')
        ).filter(applicant_count__lt=F('max_applicants')).order_by('date')

    
class RecentExamScoresView(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = RecentApplicantExamSerializer

    def get_queryset(self):
        user = self.request.user
        try:
            applicant = user.applicantprofile
        except:
            return ApplicantExam.objects.none()

        return ApplicantExam.objects.filter(applicant=applicant).order_by('-created_at')[:5]


#start exam
class StartExamView(viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = StartExamSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        from django.db import transaction

        with transaction.atomic():
            applicant_exam = serializer.save(applicant=request.user.applicantprofile)

        return Response(self.get_serializer(applicant_exam).data, status=status.HTTP_201_CREATED)
