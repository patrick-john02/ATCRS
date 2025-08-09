from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from api.models.exam import Exam, ApplicantExam
from api.serializers.AdmissionSerializer import(
    UpcomingExamSerializer,
    RecentApplicantExamSerializer
)

    

class UpcomingExamView(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        user = request.user

        try:
            applicant = user.applicantprofile
        except:
            return Response({"detail": "Applicant profile not found."}, status=400)

        today = timezone.now().date()

        upcoming_exams = Exam.objects.filter(
            is_active=True,
            is_expired=False,
            date__gte=today
        ).order_by('date')

        result = []

        for exam in upcoming_exams:
            existing_attempts = ApplicantExam.objects.filter(applicant=applicant, exam=exam).count()
            if existing_attempts < exam.max_attempts:
                result.append(exam)
                break

        serializer = UpcomingExamSerializer(result, many=True)
        return Response(serializer.data)

class RecentExamScoresView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        applicant = request.user.applicantprofile
        recent_exams = ApplicantExam.objects.filter(applicant=applicant).order_by('-created_at')[:5]
        serializer = RecentApplicantExamSerializer(recent_exams, many=True)
        return Response(serializer.data)