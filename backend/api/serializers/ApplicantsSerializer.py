from rest_framework import serializers
from django.utils import timezone
from django.db.models import F
from api.models.exam import Exam, ApplicantExam
from api.serializers.AdmissionSerializer import ExamSerializer
from api.models.auth import ApplicantProfile
from api.models.admission import Course

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
    
#applicant profile
class ApplicantProfileSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    email = serializers.EmailField(source='user.email', read_only=True)
    course_applied_name = serializers.SerializerMethodField()
    profile_photo_url = serializers.SerializerMethodField()

    class Meta:
        model = ApplicantProfile
        fields = [
            'full_name',
            'email',
            'contact_number',
            'address',
            'birthdate',
            'high_school',
            'year_graduated',
            'course_applied_name',
            'profile_photo_url',
        ]

    def get_full_name(self, obj):
        return obj.user.get_full_name()

    def get_course_applied_name(self, obj):
        if obj.course_applied:
            return obj.course_applied.name
        return None

    def get_profile_photo_url(self, obj):
        request = self.context.get('request')
        if obj.profile_photo and hasattr(obj.profile_photo, 'url'):
            if request:
                return request.build_absolute_uri(obj.profile_photo.url)
            return obj.profile_photo.url
        return None

class ApplyUpcomingExamSerializer(serializers.ModelSerializer):
    exam_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = ApplicantExam
        fields = ['exam_id', 'uuid', 'started_at', 'status', 'exam_attempt_number']
        read_only_fields = ['uuid', 'started_at', 'status', 'exam_attempt_number']

    def validate_exam_id(self, value):
        try:
            exam = Exam.objects.get(id=value, is_active=True, is_expired=False, date__gte=timezone.now().date())
        except Exam.DoesNotExist:
            raise serializers.ValidationError("Exam does not exist or is not available.")
        return value

    def create(self, validated_data):
        applicant = self.context['request'].user.profile
        exam = Exam.objects.get(id=validated_data['exam_id'])

        # Check if applicant already has an ongoing application for this exam
        existing = ApplicantExam.objects.filter(applicant=applicant, exam=exam, status__in=['not_started','in_progress']).first()
        if existing:
            return existing  # Return existing record instead of creating a new one

        # Count previous attempts
        attempt_number = ApplicantExam.objects.filter(applicant=applicant, exam=exam).count() + 1
        if attempt_number > exam.max_attempts:
            raise serializers.ValidationError("You have reached the maximum allowed attempts for this exam.")

        applicant_exam = ApplicantExam.objects.create(
            applicant=applicant,
            exam=exam,
            started_at=timezone.now(),
            status='in_progress',
            total_questions=exam.questions.count(),
            exam_attempt_number=attempt_number
        )
        return applicant_exam

class UpcomingExamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exam
        fields = [
            'uuid',
            'title',
            'date',
            'start_time',
            'end_time',
            'duration_minutes',
            'max_attempts',
            'max_applicants',
            'is_active',
            'is_expired',
        ]

#Exam Summary
class ApplicantExamSummarySerializer(serializers.ModelSerializer):
    exam_title = serializers.CharField(source='exam.title', read_only=True)
    exam_status = serializers.CharField(source='status', read_only=True)
    score = serializers.DecimalField(max_digits=5, decimal_places=2, read_only=True)
    recommendation_score = serializers.DecimalField(max_digits=5, decimal_places=2, read_only=True)
    recommended_course = serializers.CharField(source='recommended_course.name', read_only=True)
    eligible_courses = serializers.SerializerMethodField()
    total_questions = serializers.IntegerField(read_only=True)
    attempted_questions = serializers.IntegerField(read_only=True)
    correct_answers = serializers.IntegerField(read_only=True)
    exam_attempt_number = serializers.IntegerField(read_only=True)
    started_at = serializers.DateTimeField(read_only=True)
    completed_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = ApplicantExam
        fields = [
            'exam_title',
            'exam_status',
            'score',
            'recommendation_score',
            'recommended_course',
            'eligible_courses',
            'total_questions',
            'attempted_questions',
            'correct_answers',
            'exam_attempt_number',
            'started_at',
            'completed_at',
        ]

    def get_eligible_courses(self, obj):
        courses = Course.objects.filter(min_score__lte=obj.recommendation_score).order_by('-min_score')
        return [{'code': c.code, 'name': c.name, 'min_score': float(c.min_score)} for c in courses]