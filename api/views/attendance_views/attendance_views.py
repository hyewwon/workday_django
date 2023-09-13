from rest_framework.generics import GenericAPIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly

from api.serializers.attendance.attendance_serializers import AttendaceSerializer
from website.models import Attendance
from website.utils import getTokenUser
from django.db import transaction

class AttendanceView(GenericAPIView):
    '''
        출석 체크 api
    '''
    permission_classes = [IsAuthenticated]
    serializer_class = AttendaceSerializer

    def post(self, request, *args, **kwargs):
        user = getTokenUser(token = str(request.auth))
        if not user:
            return Response(
                {"message" :"토큰 정보 오류"}, status=status.HTTP_401_UNAUTHORIZED
            )
        serializer = self.get_serializer(data = request.data)   
        if serializer.is_valid(raise_exception = True):
            attend_id = serializer.validated_data["attend_id"]
            time = serializer.validated_data["time"]
            try:
                if not attend_id:
                    attend = Attendance.objects.create(
                        user = user,
                        attend_time = time
                    )
                    return Response({"message": "출근 체크되었습니다.", "attend_id": attend.id}, status=status.HTTP_202_ACCEPTED)
        
                attend = Attendance.objects.get(id = attend_id)

                if attend.leave_time:
                    return Response({"message":"체크 실패..."}, status=status.HTTP_400_BAD_REQUEST)
                
                attend.leave_time = time
                attend.save()

                return Response({"message": "퇴근 체크되었습니다."}, status=status.HTTP_202_ACCEPTED)

            
            except Exception as e:
                print(e)
                return Response({"message":"체크 실패..."}, status=status.HTTP_400_BAD_REQUEST)