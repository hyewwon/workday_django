from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly

from django.db import transaction
from django.urls import reverse
from django.contrib.auth.models import User

from api.serializers.attendance.vacation_serializers import VacationSerializer, VacationIdSerializer
from website.models import Vacation, Profile
from website.utils import getTokenUser

class VacationView(GenericAPIView):
    '''
        휴가 신청 api
    '''
    permission_classes = [IsAuthenticated]
    serializer_class = VacationSerializer

    def get(self, request, *args, **kwargs):
        user = getTokenUser(token = str(request.auth))
        if not user:
            return Response(
                {"message" :"토큰 정보 오류"}, status=status.HTTP_401_UNAUTHORIZED
            )
        department = Profile.objects.get(user = user).department
        vacation = Vacation.objects.filter(department = department).values(
            "user__last_name",
            "department__name",
            "start_date",
            "end_date"
        ).order_by("start_date")
        
        return Response({"vacation": list(vacation)}, status=status.HTTP_202_ACCEPTED)

    def post(self, request, *args, **kwargs):
        user = getTokenUser(token = str(request.auth))
        if not user:
            return Response(
                {"message" :"토큰 정보 오류"}, status=status.HTTP_401_UNAUTHORIZED
            )
        serializer = self.get_serializer(data = request.data)
        if serializer.is_valid(raise_exception = True):
            start_date = serializer.validated_data["start_date"]
            end_date = serializer.validated_data["end_date"]
            try:
                with transaction.atomic():
                    department = Profile.objects.get(user = user).department

                    Vacation.objects.create(
                        user = user,
                        department = department,
                        start_date = start_date,
                        end_date = end_date
                    )

            except Exception as e:
                print(e)
                return Response({"message":"저장 실패..."}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"message": "저장되었습니다."}, status=status.HTTP_202_ACCEPTED)

    def put(self, request, *args, **kwargs):
        user = getTokenUser(token = str(request.auth))
        if not user:
            return Response(
                {"message" :"토큰 정보 오류"}, status=status.HTTP_401_UNAUTHORIZED
            )
        serializer = self.get_serializer(data = request.data)
        if serializer.is_valid(raise_exception = True):
            start_date = serializer.validated_data["start_date"]
            end_date = serializer.validated_data["end_date"]
            vacation_id = serializer.validated_data["vacation_id"]

            if not vacation_id:
                return Response({"message":"오류 발생.."}, status=status.HTTP_400_BAD_REQUEST)
            try:
                with transaction.atomic():
                    vacation = Vacation.objects.get(id = vacation_id)

                    vacation.start_date = start_date
                    vacation.end_date = end_date
                    vacation.save()

            except Exception as e:
                print(e)
                return Response({"message":"수정 실패..."}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"message": "저장되었습니다."}, status=status.HTTP_202_ACCEPTED)

        

class VacationDeleteView(GenericAPIView):
    '''
        휴가 삭제 api
    '''
    permission_classes = [IsAuthenticated]
    serializer_class = VacationIdSerializer

    def delete(self, request, *args, **kwargs):
        user = getTokenUser(token = str(request.auth))
        if not user:
            return Response(
                {"message" :"토큰 정보 오류"}, status=status.HTTP_401_UNAUTHORIZED
            )

        serializer = self.get_serializer(data = request.data)
        if serializer.is_valid(raise_exception = True):
            vacation_id = serializer.validated_data["vacation_id"]        
            try:
                with transaction.atomic():
                    vacation = Vacation.objects.get(id = vacation_id)
                    vacation.delete()
            except Exception as e:
                print(e)
                return Response({"message":"삭제 실패..."}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({"message": "삭제되었습니다."}, status=status.HTTP_202_ACCEPTED)
