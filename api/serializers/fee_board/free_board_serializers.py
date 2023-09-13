from rest_framework import serializers

class FreeBoardSerializer(serializers.Serializer):
    title = serializers.CharField(required=True)
    content = serializers.CharField(required=True)
    board_type = serializers.CharField(required=True)
    anonymous_flag = serializers.CharField(required=True)