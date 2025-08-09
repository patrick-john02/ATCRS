from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from api.models.auth import ApplicantProfile
from api.serializers.SuperAdminUserSerializer import SuperAdminUserSerializer
from api.models.admission import (
    Course
)
from api.serializers.SuperAdminUserSerializer import CourseSerializers


class AdminUserViewSet(viewsets.ModelViewSet):
    serializer_class = SuperAdminUserSerializer
    permission_classes = [AllowAny]


    def get_queryset(self):
        return ApplicantProfile.objects.filter(user_type='admin')

class AdminApplicantsViewSet(viewsets.ModelViewSet):
    serializer_class = SuperAdminUserSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return ApplicantProfile.objects.filter(user_type='applicant')
    
class AdminManageCourses(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializers
    permission_classes = [AllowAny]