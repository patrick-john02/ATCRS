from django.contrib import admin
from api.models.auth import (
    Course,
    ApplicantProfile,
    
)

admin.site.register(Course)
admin.site.register(ApplicantProfile)