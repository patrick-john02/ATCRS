from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

USER_TYPE_CHOICES = [
    ('superadmin', 'Super Admin'),
    ('admin', 'Admin'),
    ('applicant', 'Applicant'),
]

APPLICATION_STATUS_CHOICES = [
    ('pending', 'Pending Review'),
    ('verified', 'Verified Documents'),
    ('exam_taken', 'Exam Taken'),
    ('passed', 'Passed'),
    ('failed', 'Failed'),
    ('admitted', 'Admitted'),
    ('rejected', 'Rejected'),
]

EXAM_STATUS_CHOICES = [
    ('not_taken', 'Not Taken'),
    ('in_progress', 'In Progress'),
    ('completed', 'Completed'),
]

class ApplicantProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    user_type = models.CharField(
        max_length=20, choices=USER_TYPE_CHOICES, default='applicant'
    )
    birthdate = models.DateField(null=True, blank=True)
    contact_number = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    high_school = models.CharField(max_length=100, blank=True)
    year_graduated = models.PositiveIntegerField(null=True, blank=True)
    course_applied = models.ForeignKey('api.Course', on_delete=models.SET_NULL, null=True, blank=True)
    profile_photo = models.ImageField(upload_to='applicant_photos/', blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)  
    updated_at = models.DateTimeField(auto_now=True)

    application_status = models.CharField(
        max_length=20, choices=APPLICATION_STATUS_CHOICES, default='pending', blank=True
    )
    exam_status = models.CharField(
        max_length=20, choices=EXAM_STATUS_CHOICES, default='not_taken', blank=True
    )
    exam_score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.user_type})"

    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"
        
