from django.contrib import admin
from api.models.auth import (
    ApplicantProfile,
)
from api.models.admission import Course


admin.site.register(Course)
admin.site.register(ApplicantProfile)