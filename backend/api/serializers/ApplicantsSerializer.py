from rest_framework import serializers
from django.utils import timezone
from django.db.models import F
from api.models.exam import Exam, ApplicantExam, Question
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
    exam_uuid = serializers.UUIDField(write_only=True)

    class Meta:
        model = ApplicantExam
        fields = ['exam_uuid', 'uuid', 'started_at', 'status', 'exam_attempt_number']
        read_only_fields = ['uuid', 'started_at', 'status', 'exam_attempt_number']

    def validate_exam_uuid(self, value):
        try:
            exam = Exam.objects.get(uuid=value, is_active=True, is_expired=False, date__gte=timezone.now().date())
        except Exam.DoesNotExist:
            raise serializers.ValidationError("Exam does not exist or is not available.")
        return value

    def create(self, validated_data):
        applicant = self.context['request'].user.profile
        exam = Exam.objects.get(uuid=validated_data['exam_uuid'])

        # Check if applicant already has ANY application for this exam (including completed)
        existing = ApplicantExam.objects.filter(applicant=applicant, exam=exam).first()
        
        if existing:
            # If there's a completed exam, check if they can retake
            if existing.status == 'completed':
                attempt_number = ApplicantExam.objects.filter(applicant=applicant, exam=exam).count() + 1
                if attempt_number > exam.max_attempts:
                    raise serializers.ValidationError("You have reached the maximum allowed attempts for this exam.")
            else:
                # Return existing not_started or in_progress exam
                return existing

        # Create new exam attempt
        attempt_number = ApplicantExam.objects.filter(applicant=applicant, exam=exam).count() + 1
        if attempt_number > exam.max_attempts:
            raise serializers.ValidationError("You have reached the maximum allowed attempts for this exam.")

        applicant_exam = ApplicantExam.objects.create(
            applicant=applicant,
            exam=exam,
            started_at=None,
            status='not_started',
            total_questions=exam.questions.count(),
            exam_attempt_number=attempt_number
        )
        return applicant_exam

class UpcomingExamSerializer(serializers.ModelSerializer):
    applicant_count = serializers.IntegerField(read_only=True)
    is_applied = serializers.SerializerMethodField()
    applicant_exam_uuid = serializers.SerializerMethodField()
    
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
            'max_attempts',
            'max_applicants',
            'applicant_count',
            'is_active',
            'is_expired',
            'is_applied',
            'applicant_exam_uuid',
        ]
    
    def get_is_applied(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            try:
                applicant = request.user.profile
                return ApplicantExam.objects.filter(
                    applicant=applicant,
                    exam=obj,
                    status__in=['not_started', 'in_progress']
                ).exists()
            except:
                return False
        return False
    
    def get_applicant_exam_uuid(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            try:
                applicant = request.user.profile
                exam = ApplicantExam.objects.filter(
                    applicant=applicant,
                    exam=obj,
                    status__in=['not_started', 'in_progress']
                ).first()
                return str(exam.uuid) if exam else None
            except:
                return None
        return None

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
        # Skip if recommendation_score is None
        if obj.recommendation_score is None:
            return []
        courses = Course.objects.filter(min_score__lte=obj.recommendation_score).order_by('-min_score')
        return [
            {'code': c.code, 'name': c.name, 'min_score': float(c.min_score)}
            for c in courses
        ]



# serializers - Add new serializers in ApplicantsSerializer.py

class ApplicantExamHistorySerializer(serializers.ModelSerializer):
    exam = serializers.SerializerMethodField()
    
    class Meta:
        model = ApplicantExam
        fields = [
            'uuid',
            'exam',
            'status',
            'score',
            'recommendation_score',
            'recommended_course',
            'total_questions',
            'attempted_questions',
            'correct_answers',
            'accuracy',
            'exam_attempt_number',
            'started_at',
            'completed_at',
            'created_at',
        ]
    
    def get_exam(self, instance):
        return {
            'uuid': str(instance.exam.uuid),
            'title': instance.exam.title,
            'description': instance.exam.description,
            'date': instance.exam.date.isoformat(),
        }
        
    def to_representation(self, instance):
        data = super().to_representation(instance)
        if instance.recommended_course:
            data['recommended_course'] = {
                'code': instance.recommended_course.code,
                'name': instance.recommended_course.name,
            }
        else:
            data['recommended_course'] = None
        return data


class TakeExamSerializer(serializers.ModelSerializer):
    exam_details = serializers.SerializerMethodField()
    questions = serializers.SerializerMethodField()
    
    class Meta:
        model = ApplicantExam
        fields = [
            'uuid',
            'exam_details',
            'questions',
            'started_at',
            'status',
            'total_questions',
            'attempted_questions',
            'exam_attempt_number',
        ]
        read_only_fields = ['uuid', 'started_at', 'status', 'total_questions', 'attempted_questions', 'exam_attempt_number']
    
    def get_exam_details(self, obj):
        return {
            'uuid': str(obj.exam.uuid),
            'title': obj.exam.title,
            'description': obj.exam.description,
            'duration_minutes': obj.exam.duration_minutes,
            'total_questions': obj.total_questions,
        }
    
    def get_questions(self, obj):
        questions = obj.exam.questions.all()
        result = []
        for question in questions:
            choices = question.choices.all()
            result.append({
                'uuid': str(question.uuid),
                'text': question.text,
                'question_type': question.question_type,
                'choices': [
                    {
                        'uuid': str(choice.uuid),
                        'label': choice.label,
                        'text': choice.text,
                    }
                    for choice in choices
                ]
            })
        return result


class SubmitAnswerSerializer(serializers.Serializer):
    question_uuid = serializers.UUIDField()
    choice_uuid = serializers.UUIDField()
    time_spent_seconds = serializers.IntegerField(required=False, default=0)
    
    def validate_question_uuid(self, value):
        from api.models.exam import Question
        try:
            Question.objects.get(uuid=value)
        except Question.DoesNotExist:
            raise serializers.ValidationError("Question does not exist")
        return value
    
    def validate_choice_uuid(self, value):
        from api.models.exam import Choice
        try:
            Choice.objects.get(uuid=value)
        except Choice.DoesNotExist:
            raise serializers.ValidationError("Choice does not exist")
        return value
    
    def create(self, validated_data):
        from api.models.exam import Question, Choice, ApplicantAnswer
        
        applicant_exam = self.context['applicant_exam']
        question = Question.objects.get(uuid=validated_data['question_uuid'])
        choice = Choice.objects.get(uuid=validated_data['choice_uuid'])
        
        # Check if answer already exists
        answer, created = ApplicantAnswer.objects.update_or_create(
            applicant_exam=applicant_exam,
            question=question,
            defaults={
                'selected_choice': choice,
                'is_correct': choice.is_correct,
                'time_spent_seconds': validated_data.get('time_spent_seconds', 0),
            }
        )
        
        # Update attempted questions count
        if created:
            applicant_exam.attempted_questions += 1
        
        # Update correct answers count
        if answer.is_correct:
            if not created:
                # If updating, check if previous answer was incorrect
                previous_answer = ApplicantAnswer.objects.filter(
                    applicant_exam=applicant_exam,
                    question=question
                ).first()
                if previous_answer and not previous_answer.is_correct:
                    applicant_exam.correct_answers += 1
            else:
                applicant_exam.correct_answers += 1
        
        applicant_exam.save()
        return answer


class CompleteExamSerializer(serializers.Serializer):
    def save(self):
        applicant_exam = self.context['applicant_exam']
        applicant_exam.status = 'completed'
        applicant_exam.completed_at = timezone.now()
        applicant_exam.calculate_recommendation_score()
        applicant_exam.save()
        
        # Update applicant profile
        applicant = applicant_exam.applicant
        applicant.exam_status = 'completed'
        applicant.exam_score = applicant_exam.recommendation_score
        applicant.save()
        
        return applicant_exam
    