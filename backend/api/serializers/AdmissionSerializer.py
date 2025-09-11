from rest_framework import serializers
from api.models.admission import Course
from api.models.auth import ApplicantProfile
from api.models.exam import *
from django.utils import timezone

class ChoiceSerializer(serializers.ModelSerializer):
    # allow passing question uuid when creating choice
    question = serializers.UUIDField(write_only=True)
    question_uuid = serializers.UUIDField(source="question.uuid", read_only=True)

    class Meta:
        model = Choice
        fields = ['uuid', 'question', 'question_uuid', 'label', 'text', 'is_correct', 'created_at']

    def create(self, validated_data):
        question_uuid = validated_data.pop("question")
        question = Question.objects.get(uuid=question_uuid)
        return Choice.objects.create(question=question, **validated_data)

# class QuestionSerializer(serializers.ModelSerializer):
#     # allow passing exam uuid
#     exam = serializers.UUIDField(write_only=True)
#     exam_uuid = serializers.UUIDField(source="exam.uuid", read_only=True)

#     # nested choices
#     choices = ChoiceSerializer(many=True, required=False)

#     class Meta:
#         model = Question
#         fields = [
#             'uuid',
#             'exam',
#             'exam_uuid',
#             'text',
#             'question_type',
#             'correct_choice',
#             'choices',
#             'created_at',
#         ]

#     def create(self, validated_data):
#         exam_uuid = validated_data.pop("exam")
#         exam = Exam.objects.get(uuid=exam_uuid)

#         # handle nested choices
#         choices_data = validated_data.pop("choices", [])
#         question = Question.objects.create(exam=exam, **validated_data)

#         for choice_data in choices_data:
#             Choice.objects.create(question=question, **choice_data)

#         return question

class QuestionSerializer(serializers.ModelSerializer):
    # allow passing exam uuid
    exam = serializers.UUIDField(write_only=True)
    exam_uuid = serializers.UUIDField(source="exam.uuid", read_only=True)

    # nested choices
    choices = ChoiceSerializer(many=True, required=False)

    class Meta:
        model = Question
        fields = [
            'uuid',
            'exam',
            'exam_uuid',
            'text',
            'question_type',
            'correct_choice',
            'choices',
            'created_at',
        ]

    def create(self, validated_data):
        exam_uuid = validated_data.pop("exam")
        exam = Exam.objects.get(uuid=exam_uuid)

        # handle nested choices
        choices_data = validated_data.pop("choices", [])
        question = Question.objects.create(exam=exam, **validated_data)

        for choice_data in choices_data:
            Choice.objects.create(question=question, **choice_data)

        return question

    def update(self, instance, validated_data):
        choices_data = validated_data.pop("choices", [])
        
        # Update question fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Handle choices update
        if choices_data:
            # Delete existing choices
            instance.choices.all().delete()
            
            # Create new choices
            for choice_data in choices_data:
                Choice.objects.create(question=instance, **choice_data)

        return instance
    

class ExamSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, required=False)

    class Meta:
        model = Exam
        fields = [
            'uuid', 'slug', 'title', 'description', 'date',
            'start_time', 'end_time', 'duration_minutes', 'access_code',
            'is_active', 'questions', 'created_at', 'updated_at'
        ]
        read_only_fields = ['uuid', 'slug', 'created_at', 'updated_at']

    def create(self, validated_data):
        questions_data = validated_data.pop("questions", [])
        exam = Exam.objects.create(**validated_data)

        for question_data in questions_data:
            choices_data = question_data.pop("choices", [])
            question = Question.objects.create(exam=exam, **question_data)
            for choice_data in choices_data:
                Choice.objects.create(question=question, **choice_data)

        return exam


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