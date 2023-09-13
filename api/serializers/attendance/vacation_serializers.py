from rest_framework import serializers

class VacationSerializer(serializers.Serializer):
    vacation_id = serializers.CharField(allow_null=True)
    start_date = serializers.CharField(required=True)
    end_date = serializers.CharField(allow_null=True)

class VacationIdSerializer(serializers.Serializer):
    vacation_id = serializers.CharField(required=True)