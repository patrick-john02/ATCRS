from rest_framework import serializers
from django.contrib.auth.models import User
from api.models.auth import ApplicantProfile
from api.models.admission import Course


# class SuperAdminUserSerializer(serializers.ModelSerializer):
#     username = serializers.CharField(source='user.username')
#     email = serializers.EmailField(source='user.email')
#     first_name = serializers.CharField(source='user.first_name')
#     last_name = serializers.CharField(source='user.last_name')
#     password = serializers.CharField(write_only=True, min_length=6)

#     class Meta:
#         model = ApplicantProfile
#         fields = [
#             'id',
#             'username',
#             'email',
#             'first_name',
#             'last_name',
#             'password',
#             'contact_number',
#             'address',
#             'birthdate',
#             'high_school',
#             'year_graduated',
#             'application_status',
#             'exam_status',
#             'exam_score',
#         ]

#     def create(self, validated_data):
#         user_data = validated_data.pop('user')
#         password = validated_data.pop('password')

#         user = User.objects.create(**user_data)
#         user.set_password(password)
#         user.save()

#         profile = ApplicantProfile.objects.create(user=user, user_type='admin', **validated_data)
#         return profile




    # def update(self, instance, validated_data):
    #     user_data = validated_data.pop('user', {})
    #     user = instance.user
    #     for attr, value in user_data.items():
    #         setattr(user, attr, value)
    #     user.save()

    #     for attr, value in validated_data.items():
    #         setattr(instance, attr, value)
    #     instance.save()
    #     return instance
    
    
# serializers
class SuperAdminUserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    email = serializers.EmailField(source='user.email')
    first_name = serializers.CharField(source='user.first_name')
    last_name = serializers.CharField(source='user.last_name')
    password = serializers.CharField(write_only=True, min_length=6, required=False)

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
            'birthdate',
            'high_school',
            'year_graduated',
            'application_status',
            'exam_status',
            'exam_score',
        ]

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        password = validated_data.pop('password')

        user = User.objects.create(**user_data)
        user.set_password(password)
        user.save()

        profile = ApplicantProfile.objects.create(
            user=user, 
            user_type='applicant',  # Changed from 'admin' to 'applicant'
            **validated_data
        )
        return profile

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', {})
        password = validated_data.pop('password', None)
        
        user = instance.user
        for attr, value in user_data.items():
            setattr(user, attr, value)
        
        if password:
            user.set_password(password)
        
        user.save()

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
    
    


class SuperAdminUserCreateSerializer(serializers.ModelSerializer):
    """For creating/updating admins"""
    username = serializers.CharField()
    email = serializers.EmailField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
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
            'birthdate',
            'high_school',
            'year_graduated',
        ]

    def create(self, validated_data):
        username = validated_data.pop('username')
        email = validated_data.pop('email')
        first_name = validated_data.pop('first_name')
        last_name = validated_data.pop('last_name')
        password = validated_data.pop('password')

        user = User.objects.create(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name
        )
        user.set_password(password)
        user.save()

        profile = ApplicantProfile.objects.create(
            user=user,
            user_type='admin',
            **validated_data
        )
        return profile

    def update(self, instance, validated_data):
        user = instance.user
        user.username = validated_data.pop('username', user.username)
        user.email = validated_data.pop('email', user.email)
        user.first_name = validated_data.pop('first_name', user.first_name)
        user.last_name = validated_data.pop('last_name', user.last_name)

        password = validated_data.pop('password', None)
        if password:
            user.set_password(password)
        user.save()

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

class CourseSerializers(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'