from rest_framework import serializers
from api.models.admission import Course
from api.models.auth import ApplicantProfile
from api.models.exam import *
from django.utils import timezone

# class ChoiceSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Choice
#         fields = ['uuid', 'question', 'label', 'text', 'is_correct', 'created_at']
#         read_only_fields = ['uuid', 'question', 'created_at']

class ChoiceSerializer(serializers.ModelSerializer):
    question_uuid = serializers.UUIDField(write_only=True, required=False)
    
    class Meta:
        model = Choice
        fields = ['uuid', 'question', 'question_uuid', 'label', 'text', 'is_correct', 'created_at']
        read_only_fields = ['uuid', 'question', 'created_at']

    def create(self, validated_data):
        question_uuid = validated_data.pop('question_uuid', None)
        if question_uuid:
            question = Question.objects.get(uuid=question_uuid)
            validated_data['question'] = question
        return super().create(validated_data)


# class QuestionSerializer(serializers.ModelSerializer):
#     choices = ChoiceSerializer(many=True, required=False)

#     class Meta:
#         model = Question
#         fields = [
#             'uuid',
#             'exam',
#             'text',
#             'question_type',
#             'choices',
#             'created_at',
#         ]
#         read_only_fields = ['uuid', 'exam', 'choices', 'created_at']


class QuestionSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True, required=False)
    exam_uuid = serializers.UUIDField(write_only=True, required=False)

    class Meta:
        model = Question
        fields = [
            'uuid',
            'exam',
            'exam_uuid',
            'text',
            'question_type',
            'choices',
            'created_at',
        ]
        read_only_fields = ['uuid', 'exam', 'choices', 'created_at']

    def create(self, validated_data):
        exam_uuid = validated_data.pop('exam_uuid', None)
        if exam_uuid:
            exam = Exam.objects.get(uuid=exam_uuid)
            validated_data['exam'] = exam
        return super().create(validated_data)


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

# class UpcomingExamSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Exam
#         fields = [
#             'uuid',
#             'title',
#             'description',
#             'date',
#             'start_time',
#             'end_time',
#             'duration_minutes',
#             'access_code',
#             'max_attempts',
#         ]
        
class ApplyUpcomingExamSerializer(serializers.ModelSerializer):
    exam_id = serializers.IntegerField(write_only=True)
    exam_title = serializers.CharField(source='exam.title', read_only=True)
    status = serializers.CharField(read_only=True)
    
    class Meta:
        model = ApplicantExam
        fields = ['uuid', 'exam_id', 'exam_title', 'status', 'created_at']
        read_only_fields = ['uuid', 'status', 'created_at']
    
    def validate_exam_id(self, value):
        try:
            exam = Exam.objects.get(id=value)
        except Exam.DoesNotExist:
            raise serializers.ValidationError("Exam does not exist")
        
        # Check if exam is active
        if not exam.is_active or exam.is_expired:
            raise serializers.ValidationError("This exam is no longer available")
        
        # Check if exam is full
        applicant_count = ApplicantExam.objects.filter(exam=exam).count()
        if applicant_count >= exam.max_applicants:
            raise serializers.ValidationError("This exam has reached maximum capacity")
        
        # Check if applicant already applied
        applicant = self.context['request'].user.profile
        if ApplicantExam.objects.filter(applicant=applicant, exam=exam).exists():
            raise serializers.ValidationError("You have already applied to this exam")
        
        return value
    
    def create(self, validated_data):
        exam_id = validated_data.pop('exam_id')
        exam = Exam.objects.get(id=exam_id)
        applicant = self.context['request'].user.profile
        
        applicant_exam = ApplicantExam.objects.create(
            applicant=applicant,
            exam=exam,
            status='not_started',
            total_questions=exam.questions.count()
        )
        return applicant_exam
    

class UpcomingExamSerializer(serializers.ModelSerializer):
    available_slots = serializers.SerializerMethodField()
    is_applied = serializers.SerializerMethodField()
    
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
            'max_applicants',
            'available_slots',
            'is_applied',
        ]
    
    def get_available_slots(self, obj):
        applicant_count = ApplicantExam.objects.filter(exam=obj).count()
        return obj.max_applicants - applicant_count
    
    def get_is_applied(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            try:
                return ApplicantExam.objects.filter(
                    applicant=request.user.profile,
                    exam=obj
                ).exists()
            except:
                return False
        return False

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
        
class AdminResultSerializer(serializers.ModelSerializer):
    applicant_name = serializers.CharField(source='applicant.user.get_full_name', read_only=True)
    applicant_email = serializers.EmailField(source='applicant.user.email', read_only=True)
    exam_title = serializers.CharField(source='exam.title', read_only=True)
    exam_date = serializers.DateField(source='exam.date', read_only=True)
    recommended_course_name = serializers.CharField(source='recommended_course.name', read_only=True)
    
    class Meta:
        model = ApplicantExam
        fields = [
            'uuid',
            'applicant_name',
            'applicant_email',
            'exam_title',
            'exam_date',
            'score',
            'recommendation_score',
            'accuracy',
            'total_questions',
            'attempted_questions',
            'correct_answers',
            'recommended_course_name',
            'exam_attempt_number',
            'completed_at',
            'created_at',
        ]