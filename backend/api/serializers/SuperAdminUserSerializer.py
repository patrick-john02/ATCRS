from rest_framework import serializers
from django.contrib.auth.models import User
from api.models.auth import ApplicantProfile


class SuperAdminUserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True)
    email = serializers.EmailField(write_only=True)
    first_name = serializers.CharField(write_only=True)
    last_name = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = ApplicantProfile
        fields = [
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'password',
            'contact_number',
            'address',
        ]

    def create(self, validated_data):
        # Extract user fields
        user_data = {
            'username': validated_data.pop('username'),
            'email': validated_data.pop('email'),
            'first_name': validated_data.pop('first_name'),
            'last_name': validated_data.pop('last_name'),
        }
        password = validated_data.pop('password')

        # Create User instance
        user = User.objects.create(**user_data)
        user.set_password(password)
        user.save()

        # Create admin profile
        profile = ApplicantProfile.objects.create(
            user=user,
            user_type='admin',
            **validated_data
        )
        return profile

    def update(self, instance, validated_data):
        user = instance.user
        user.first_name = validated_data.pop('first_name', user.first_name)
        user.last_name = validated_data.pop('last_name', user.last_name)
        user.email = validated_data.pop('email', user.email)
        user.save()

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
