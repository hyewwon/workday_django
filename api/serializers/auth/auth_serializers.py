from rest_framework import serializers
from django.contrib.auth.models import User


class UserSerializer(serializers.Serializer):
    class Meta:
        model = User
        fields = ("id", "username")

class UsernameSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)

class EmailSerializer(serializers.Serializer):
    email = serializers.CharField(required=True)

class RegisterSerializer(serializers.Serializer):
    membername = serializers.CharField(required=True)
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    check_password = serializers.CharField(required=True)
    email = serializers.CharField(required=True)
    phone_no = serializers.CharField(required=True)
    department_id = serializers.CharField(required=True)


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    