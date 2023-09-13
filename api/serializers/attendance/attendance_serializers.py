from rest_framework import serializers

class AttendaceSerializer(serializers.Serializer):
    attend_id = serializers.CharField(allow_null = True)
    time = serializers.CharField(required=True)
    