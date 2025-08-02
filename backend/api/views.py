from django.shortcuts import render
from rest_framework.permissions import AllowAny
from rest_framework import mixins,viewsets
# from django.contrib.auth.models import User
from api.models.auth import ApplicantProfile
from api.serializers.RegistrationSerializers import RegisterSerializer
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from api.serializers.AdmissionSerializer import UserSerializers
from rest_framework.response import Response
from rest_framework.exceptions import NotFound

User = get_user_model()

class CurrentUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if hasattr(request.user, 'profile'):
            serializer = UserSerializers(request.user.profile)
            return Response(serializer.data)
        return Response({
        'id': request.user.id,
        'username': request.user.username,
        'email': request.user.email,
        'first_name': request.user.first_name,
        'last_name': request.user.last_name,
        'user_type': 'superadmin' if request.user.is_superuser else 'admin', 
    })


class RegistrationView(mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = RegisterSerializer
    queryset = ApplicantProfile.objects.all()
    permission_classes = [AllowAny]
    