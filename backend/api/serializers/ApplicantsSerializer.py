from rest_framework import serializers
from django.utils import timezone
from django.db.models import F
from api.models.exam import Exam, ApplicantExam
from api.serializers.AdmissionSerializer import ExamSerializer

class ApplicantExamSerializer(serializers.ModelSerializer):
    exam_access_code = serializers.CharField(write_only=True)
    exam = ExamSerializer(read_only=True)

    class Meta:
        model = ApplicantExam
        fields = [
            'uuid', 'applicant', 'exam', 'exam_access_code', 'started_at', 'completed_at',
            'score', 'recommendation_score', 'status', 'total_questions',
            'attempted_questions', 'correct_answers', 'accuracy',
            'exam_attempt_number', 'created_at'
        ]
        read_only_fields = ['uuid', 'created_at', 'started_at', 'status', 'total_questions']

    def create(self, validated_data):
        access_code = validated_data.pop('exam_access_code')
        applicant = validated_data.get('applicant')

        # Validate exam access code
        try:
            exam = Exam.objects.get(access_code=access_code, is_active=True)
        except Exam.DoesNotExist:
            raise serializers.ValidationError("Invalid or inactive access code.")

        # Check max applicants dynamically from exam.max_applicants
        current_applicants = ApplicantExam.objects.filter(exam=exam).count()
        if current_applicants >= exam.max_applicants:
            raise serializers.ValidationError(
                f"This exam has reached the maximum number of applicants ({exam.max_applicants})."
            )

        # Count previous attempts for this applicant
        attempt_num = ApplicantExam.objects.filter(applicant=applicant, exam=exam).count() + 1

        # Create ApplicantExam instance
        applicant_exam = ApplicantExam(
            exam=exam,
            applicant=applicant,
            started_at=timezone.now(),
            status='in_progress',
            total_questions=exam.questions.count(),
            exam_attempt_number=attempt_num
        )
        applicant_exam.save()
        return applicant_exam


#start exams
class StartExamSerializer(serializers.ModelSerializer):
    exam_access_code = serializers.CharField(write_only=True)
    exam = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = ApplicantExam
        fields = [
            "uuid", "applicant", "exam", "exam_access_code",
            "started_at", "status", "exam_attempt_number"
        ]
        read_only_fields = ["uuid", "started_at", "status", "exam_attempt_number"]

    def create(self, validated_data):
        access_code = validated_data.pop("exam_access_code")
        applicant = validated_data.get("applicant")

        # Validate exam access code
        try:
            exam = Exam.objects.get(access_code=access_code, is_active=True)
        except Exam.DoesNotExist:
            raise serializers.ValidationError("Invalid or inactive access code.")


        current_applicants = ApplicantExam.objects.filter(exam=exam).count()
        if current_applicants >= exam.max_applicants:
            raise serializers.ValidationError(
                f"This exam has reached the maximum number of applicants ({exam.max_applicants})."
            )


        attempt_num = ApplicantExam.objects.filter(applicant=applicant, exam=exam).count() + 1
        if attempt_num > exam.max_attempts:
            raise serializers.ValidationError(
                f"You have reached the maximum allowed attempts ({exam.max_attempts}) for this exam."
            )

        applicant_exam = ApplicantExam.objects.create(
            exam=exam,
            applicant=applicant,
            started_at=timezone.now(),
            status="in_progress",
            total_questions=exam.questions.count(),
            exam_attempt_number=attempt_num
        )

        return applicant_exam