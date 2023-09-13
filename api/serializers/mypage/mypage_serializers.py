from rest_framework import serializers

class MyPageSerializer(serializers.Serializer):
    user_name = serializers.CharField(required=True)
    email = serializers.CharField(required=True)
    phone_no = serializers.CharField(required=True)
    note = serializers.CharField(allow_null=True)
    
class MyPagePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password1 = serializers.CharField(required=True)
    new_password2 = serializers.CharField(required=True)