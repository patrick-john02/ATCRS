from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from api.models.auth import ApplicantProfile
from api.permissions import IsAdmin, IsSuperAdmin
from api.serializers.SuperAdminUserSerializer import (
    SuperAdminUserSerializer,
    SuperAdminUserCreateSerializer,
)
from api.models.admission import (
    Course
)
from api.serializers.SuperAdminUserSerializer import CourseSerializers


class SuperAdminUserViewSet(viewsets.ModelViewSet):
    queryset = ApplicantProfile.objects.filter(user_type="admin")
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        if self.action in ["create", "update", "partial_update"]:
            return SuperAdminUserCreateSerializer
        return SuperAdminUserSerializer

class SuperAdminApplicantsViewSet(viewsets.ModelViewSet):
    serializer_class = SuperAdminUserSerializer
    permission_classes = [AllowAny]
    # permission_classes = [IsAdmin, IsSuperAdmin, IsAuthenticated ]
    
    def get_queryset(self):
        queryset = ApplicantProfile.objects.filter(user_type = 'applicant').order_by('created_at')
        
        is_verified_param = self.request.query_params.get('is_verified')
        if is_verified_param is not None:
            if is_verified_param.lower() == 'true':
                queryset = queryset.filter(is_verified=True)
            if is_verified_param.lower() == 'false':
                queryset = queryset.filter(is_verified = False)
        return queryset
    
class SuperAdminManageCourses(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializers
    permission_classes = [AllowAny]
    # permission_classes = [IsAdmin, IsSuperAdmin, IsAuthenticated ]