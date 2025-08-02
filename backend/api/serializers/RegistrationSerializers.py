from rest_framework import serializers
from api.models.auth import ApplicantProfile, Course
from django.contrib.auth.models import User

class RegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    email = serializers.EmailField(source='user.email')
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')

    password = serializers.CharField(write_only=True)
    user_type = serializers.ChoiceField(choices=[('applicant', 'Applicant')])
    birthdate = serializers.DateField(required=False)
    contact_number = serializers.CharField(required=False, allow_blank=True)
    address = serializers.CharField(required=False, allow_blank=True)
    high_school = serializers.CharField(required=False, allow_blank=True)
    year_graduated = serializers.IntegerField(required=False)
    course_applied = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all(), required=False)
    profile_photo = serializers.ImageField(required=False)

    class Meta:
        model = ApplicantProfile
        fields = [
            'username', 'email', 'password', 'first_name', 'last_name',
            'user_type', 'birthdate', 'contact_number', 'address',
            'high_school', 'year_graduated', 'course_applied', 'profile_photo'
        ]

    def validate(self, data):
        user_data = data.get('user', {})
        username = user_data.get('username')
        email = user_data.get('email')

        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError({'username': 'This username is already taken.'})

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({'email': 'This email is already in use.'})

        return data

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        password = validated_data.pop('password')
        user_type = validated_data.pop('user_type')

        user = User(**user_data)
        user.set_password(password)
        user.save()

        profile = ApplicantProfile.objects.create(
            user=user,
            user_type=user_type,
            **validated_data
        )
        return profile
