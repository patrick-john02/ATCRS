from rest_framework import serializers
from api.models.auth import ApplicantProfile, Course
from django.contrib.auth.models import User

class RegisterSerializer(serializers.Serializer):
    # User fields
    username = serializers.CharField()
    email = serializers.EmailField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    password = serializers.CharField(write_only=True)

    # Profile fields
    user_type = serializers.ChoiceField(choices=[('applicant', 'Applicant')])
    birthdate = serializers.DateField(required=False)
    contact_number = serializers.CharField(required=False, allow_blank=True)
    address = serializers.CharField(required=False, allow_blank=True)
    high_school = serializers.CharField(required=False, allow_blank=True)
    year_graduated = serializers.IntegerField(required=False)

    def validate(self, data):
        if User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError({'username': 'This username is already taken.'})
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError({'email': 'This email is already in use.'})
        return data

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data.pop('username'),
            email=validated_data.pop('email'),
            password=validated_data.pop('password'),
            first_name=validated_data.pop('first_name'),
            last_name=validated_data.pop('last_name'),
        )

        profile = ApplicantProfile.objects.create(
            user=user,
            **validated_data
        )
        return profile

    def to_representation(self, instance):
        return {
            "id": instance.id,
            "username": instance.user.username,
            "email": instance.user.email,
            "first_name": instance.user.first_name,
            "last_name": instance.user.last_name,
            "user_type": instance.user_type,
            "birthdate": instance.birthdate,
            "contact_number": instance.contact_number,
            "address": instance.address,
            "high_school": instance.high_school,
            "year_graduated": instance.year_graduated,
        }
