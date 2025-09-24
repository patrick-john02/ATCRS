from rest_framework import serializers
from api.models.admission import Course
from api.models.auth import ApplicantProfile
from api.models.exam import *
from django.utils import timezone

class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ['uuid', 'question', 'label', 'text', 'is_correct', 'created_at']
        read_only_fields = ['uuid', 'question', 'created_at']


class QuestionSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True, required=False)

    class Meta:
        model = Question
        fields = [
            'uuid',
            'exam',
            'text',
            'question_type',
            'choices',
            'created_at',
        ]
        read_only_fields = ['uuid', 'exam', 'choices', 'created_at']


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
    recommended_course = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = ApplicantExam
        fields = [
            'uuid',
            'applicant',
            'exam',
            'exam_access_code',
            'started_at',
            'completed_at',
            'score',
            'recommendation_score',
            'accuracy',
            'status',
            'total_questions',
            'attempted_questions',
            'correct_answers',
            'exam_attempt_number',
            'recommended_course',
            'created_at',
        ]
        read_only_fields = [
            'uuid',
            'created_at',
            'started_at',
            'status',
            'total_questions',
            'recommended_course',
        ]

    def create(self, validated_data):
        access_code = validated_data.pop('exam_access_code')
        applicant = validated_data.get('applicant')


        try:
            exam = Exam.objects.get(access_code=access_code, is_active=True)
        except Exam.DoesNotExist:
            raise serializers.ValidationError("Invalid or inactive access code.")


        attempt_num = ApplicantExam.objects.filter(applicant=applicant, exam=exam).count() + 1


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

    def update(self, instance, validated_data):
        """
        Use this method when updating an exam (e.g., completing it and saving score),
        and automatically assign a recommended course based on recommendation_score.
        """
        instance.score = validated_data.get('score', instance.score)
        instance.correct_answers = validated_data.get('correct_answers', instance.correct_answers)
        instance.attempted_questions = validated_data.get('attempted_questions', instance.attempted_questions)
        instance.completed_at = validated_data.get('completed_at', timezone.now())
        instance.status = 'completed'

        if instance.total_questions > 0:
            instance.recommendation_score = round((instance.correct_answers / instance.total_questions) * 100, 2)
            instance.accuracy = instance.recommendation_score
        else:
            instance.recommendation_score = 0
            instance.accuracy = 0

        recommended_course = Course.objects.filter(min_score__lte=instance.recommendation_score).order_by('-min_score').first()
        
        # if recommended_course:
        #     instance.recommended_course = recommended_course
        #     instance.save()
        
        #when course_applied to update automatically
        if recommended_course:
            instance.applicant.course_applied = recommended_course
            instance.applicant.save()
        
        
        instance.save()
        return instance

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