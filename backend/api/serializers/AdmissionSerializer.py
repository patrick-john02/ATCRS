from rest_framework import serializers
from api.models.admission import Course
from api.models.auth import ApplicantProfile
from api.models.exam import *
from django.utils import timezone

class ChoiceSerializer(serializers.ModelSerializer):
    question = serializers.UUIDField(source="question.uuid", read_only=True)
    class Meta:
        model = Choice
        fields = ['uuid', 'question', 'label', 'text', 'is_correct']

class QuestionSerializer(serializers.ModelSerializer):
    exam = serializers.UUIDField(source="exam.uuid", read_only=True)
    choices = ChoiceSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ['uuid', 'exam', 'text', 'question_type', 'correct_choice', 'choices', 'created_at']

class ExamSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Exam
        fields = [
            'uuid', 'slug', 'title', 'description', 'date',
            'start_time', 'end_time', 'duration_minutes', 'access_code',
            'is_active', 'questions', 'created_at', 'updated_at'
        ]
        read_only_fields = ['uuid', 'slug', 'created_at', 'updated_at']

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

        # Validate access code
        try:
            exam = Exam.objects.get(access_code=access_code, is_active=True)
        except Exam.DoesNotExist:
            raise serializers.ValidationError("Invalid or inactive access code.")

        # Count previous attempts
        attempt_num = ApplicantExam.objects.filter(applicant=applicant, exam=exam).count() + 1

        # Create new ApplicantExam
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


class ApplicantAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicantAnswer
        fields = '__all__'


class CourseSerializers(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'

class UpcomingExamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exam
        fields = [
            'uuid',
            'title',
            'description',
            'date',
            'start_time',
            'end_time',
            'duration_minutes',
            'access_code',
            'max_attempts',
        ]

class RecentApplicantExamSerializer(serializers.ModelSerializer):
    exam_title = serializers.CharField(source='exam.title')
    exam_date = serializers.DateField(source='exam.date')

    class Meta:
        model = ApplicantExam
        fields = [
            'uuid',
            'exam_title',
            'exam_date',
            'score',
            'recommendation_score',
            'status',
            'accuracy',
            'exam_attempt_number',
            'created_at',
        ]

class UserSerializers(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)

    class Meta:
        model = ApplicantProfile
        fields = [
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'user_type',
            'birthdate',
            'contact_number',
            'address',
            'high_school',
            'year_graduated',
            'course_applied',
            'profile_photo',
            'application_status',
            'exam_status',
            'exam_score',
        ]

class ApplicationForAdmissionSerializers(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    first_name = serializers.CharField(source='user.first_name', read_only=True)
    last_name = serializers.CharField(source='user.last_name', read_only=True)

    class Meta:
        model = ApplicantProfile
        fields = [
            'id',
            'course_applied',
            
        ]