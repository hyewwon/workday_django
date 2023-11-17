from rest_framework import serializers
from django.contrib.auth.models import User
from website.models import Profile, Department
from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile
from io import BytesIO

class UserSerializer(serializers.Serializer):
    class Meta:
        model = User
        fields = ("id", "email", "username")

class UsernameSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)

class EmailSerializer(serializers.Serializer):
    email = serializers.CharField(required=True)

class RegisterSerializer(serializers.Serializer):
    membername = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    check_password = serializers.CharField(required=True)
    email = serializers.CharField(required=True)
    phone_no = serializers.CharField(required=True)
    department_id = serializers.CharField(required=True)
    company_id = serializers.CharField(required=True)
    image = serializers.ImageField(use_url=True, allow_null=True)

class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(required=True)
    password = serializers.CharField(required=False)
    login_type = serializers.CharField(required=True)

