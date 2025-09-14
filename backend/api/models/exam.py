from django.db import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.utils.text import slugify

from api.models.auth import ApplicantProfile
import uuid

EXAM_PROGRESS_CHOICES = [
    ('not_started', 'Not Started'),
    ('in_progress', 'In Progress'),
    ('completed', 'Completed'),
]

QUESTION_TYPES = [
    ('mcq', 'Multiple Choice'),
    ('essay', 'Essay'),
    ('true_false', 'True/False'),
]

class Exam(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    title = models.CharField(max_length=100, verbose_name="Exam Title", help_text="Title of the exam")
    description = models.TextField(blank=True, verbose_name="Description", help_text="Optional description of the exam")
    date = models.DateField(verbose_name="Exam Date")
    start_time = models.TimeField(null=True, blank=True, verbose_name="Start Time")
    end_time = models.TimeField(null=True, blank=True, verbose_name="End Time")
    duration_minutes = models.PositiveIntegerField(verbose_name="Duration (minutes)", help_text="Duration of the exam in minutes")
    is_active = models.BooleanField(default=True, verbose_name="Is Active")
    access_code = models.CharField(max_length=10, blank=True, verbose_name="Access Code", help_text="Code required to access the exam")
    max_attempts = models.PositiveIntegerField(default=1, verbose_name="Max Attempts", help_text="Maximum number of allowed attempts")
    is_expired = models.BooleanField(default=False, verbose_name="Is Expired", help_text="Marks whether the exam has expired")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.title}-{uuid.uuid4().hex[:6]}")
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-date']


class Question(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPES, default='mcq')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.exam.title} - {self.text[:50]}"

    class Meta:
        ordering = ['id']


class Choice(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='choices')
    label = models.CharField(
        max_length=1,
        validators=[RegexValidator(r'^[A-Z]$', 'Only single uppercase letters (A-Z) are allowed')]
    )
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('question', 'label')
        ordering = ['label']

    def __str__(self):
        return f"{self.label}. {self.text}"


class ApplicantExam(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    applicant = models.ForeignKey(ApplicantProfile, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    recommendation_score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    status = models.CharField(max_length=20, choices=EXAM_PROGRESS_CHOICES, default='not_started')
    total_questions = models.PositiveIntegerField(default=0)
    attempted_questions = models.PositiveIntegerField(default=0)
    correct_answers = models.PositiveIntegerField(default=0)
    accuracy = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    exam_attempt_number = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('applicant', 'exam')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.applicant.user.get_full_name()} - {self.exam.title}"

    def calculate_recommendation_score(self):
        if self.total_questions == 0:
            self.recommendation_score = 0
        else:
            self.recommendation_score = round((self.correct_answers / self.total_questions) * 100, 2)
            self.accuracy = self.recommendation_score
        self.save()


class ApplicantAnswer(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    applicant_exam = models.ForeignKey(ApplicantExam, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_choice = models.ForeignKey(Choice, on_delete=models.SET_NULL, null=True, blank=True)
    is_correct = models.BooleanField(default=False)
    answered_at = models.DateTimeField(auto_now_add=True)
    time_spent_seconds = models.PositiveIntegerField(null=True, blank=True, verbose_name="Time Spent (sec)")
    suspected_flag = models.BooleanField(default=False)
    tab_switch_count = models.PositiveIntegerField(default=0, verbose_name="Tab Switches")
    multiple_submission_flag = models.BooleanField(default=False, verbose_name="Multiple Submissions")

    class Meta:
        unique_together = ('applicant_exam', 'question')

    def save(self, *args, **kwargs):
        if self.selected_choice and self.question.correct_choice:
            self.is_correct = self.selected_choice == self.question.correct_choice

        if self.tab_switch_count > 3 or self.time_spent_seconds > 600:  # adjust threshold as needed
            self.suspected_flag = True

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Answer to {self.question.text[:30]} - Correct: {self.is_correct}"


# new update v1
# Added is_expired to Exam
# Added max_attempts to Exam
# Added tab_switch_count, multiple_submission_flag to ApplicantAnswer
# Added detection logic for cheating in ApplicantAnswer.save()
# Added verbose_name and help_text to critical fields for Django Admin clarity

