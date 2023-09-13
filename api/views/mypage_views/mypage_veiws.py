from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly

from django.db import transaction
from django.urls import reverse
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User

from api.serializers.mypage.mypage_serializers import MyPageSerializer, MyPagePasswordSerializer
from website.models import Profile
from website.utils import getTokenUser, validate_password

class MyPageEditView(GenericAPIView):
    '''
        회원 정보 수정 api
    '''
    permission_classes = [IsAuthenticated]
    serializer_class = MyPageSerializer

    def put(self, request, *args, **kwargs):
        user = getTokenUser(token=str(request.auth))
        if not user:
            return Response(
                {"message": "토큰 정보 오류"}, status=status.HTTP_401_UNAUTHORIZED
            )

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user_name = serializer.validated_data["user_name"]
            email = serializer.validated_data["email"]
            phone_no = serializer.validated_data["phone_no"]
            note = serializer.validated_data["note"]

            try:
                with transaction.atomic():
                    profile = Profile.objects.get(user = user)

                    user.last_name = user_name
                    user.email = email
                    profile.phone_no = phone_no
                    profile.note = note

                    user.save()
                    profile.save()

            except:
                return Response({"message":"수정 실패..."}, status=status.HTTP_400_BAD_REQUEST)

        
        return Response({"message": "수정되었습니다.", "next" : reverse("website:mypage")}, status=status.HTTP_202_ACCEPTED)

class MyPageEditPasswordView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = MyPagePasswordSerializer

    def put(self, request, *args, **kwargs):
        user = getTokenUser(token = str(request.auth))
        if not user:
            return Response(
                {"message": "토큰 정보 오류"}, status=status.HTTP_401_UNAUTHORIZED
            )
        user = User.objects.get(id = user.id)
        serializer = self.get_serializer(data = request.data)
        if serializer.is_valid(raise_exception=True):
            old_password = serializer.validated_data["old_password"]
            new_password1 = serializer.validated_data["new_password1"]
            new_password2 = serializer.validated_data["new_password2"]

            if not check_password(old_password, user.password):
                return Response({"message": "현재 비밀번호가 일치하지 않습니다."}, status=status.HTTP_400_BAD_REQUEST)

            if not validate_password(new_password1):
                return Response({"message": "유효한 비밀번호가 아닙니다."}, status=status.HTTP_400_BAD_REQUEST)
            
            if new_password1 != new_password2:
                return Response({"message" : "새로운 비밀번호 확인이 다릅니다."}, status=status.HTTP_400_BAD_REQUEST)
            
            try:
                with transaction.atomic():
                    user.set_password(new_password1)
                    user.save()

                user = authenticate(username=user.username, password=new_password1)
                login(request, user)

            except:
                return Response({"message": "변경 실패"}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({"message": "변경되었습니다."}, status=status.HTTP_202_ACCEPTED)