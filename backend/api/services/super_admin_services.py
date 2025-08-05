from rest_framework import viewsets
from api.models.auth import ApplicantProfile
from api.serializers.SuperAdminUserSerializer import SuperAdminUserSerializer


class AdminUserViewSet(viewsets.ModelViewSet):
    serializer_class = SuperAdminUserSerializer

    def get_queryset(self):
        return ApplicantProfile.objects.filter(user_type='admin')

class AdminUserViewSet(viewsets.ModelViewSet):
    serializer_class = SuperAdminUserSerializer

    def get_queryset(self):
        return ApplicantProfile.objects.filter(user_type='applicants')