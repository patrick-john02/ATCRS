from django.contrib import admin
from api.models.auth import (
    ApplicantProfile,
)
from api.models.admission import Course
from api.models.exam import Exam


admin.site.register(Course)
admin.site.register(ApplicantProfile)
admin.site.register(Exam)