from rest_framework import serializers
from .models import Course,User,Schedule,Lesson,Profile
from django.contrib.auth.models import User



# User Serializer
class UserSerializer(serializers.ModelSerializer):
    # Add a password field, make it write-only
    # prevents allowing 'read' capabilities (returning the password via api response)
    password = serializers.CharField(write_only=True)  

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']  ,
        )
      
        return user

# Profile Serializer#
class ProfileSerializer(serializers.ModelSerializer):
    user_profile = UserSerializer(read_only=True)
    class Meta:
        model = Profile
        fields = ('is_student')

    def create(self, validated_data):
            profile_type = Profile.objects.create_profile(
            is_student=validated_data['profile'],
        
            )
        
            return profile_type
        
# Course Serializer
class CourseSerializer(serializers.ModelSerializer):
    teacher =  serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = Course
        fields = '__all__'

# Schedule Serializer
class ScheduleSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Schedule
        fields = '__all__'


# Lesson Serializer
class LessonSerializer(serializers.ModelSerializer):
    lessons =  ScheduleSerializer(many=True,read_only=True)
    class Meta:
        model = Lesson
        fields = '__all__'