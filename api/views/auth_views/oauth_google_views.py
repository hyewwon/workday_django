from django.conf import settings
from django.shortcuts import render,  redirect
from django.contrib.auth.models import User
from allauth.socialaccount.models import SocialAccount, SocialApp
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly
from rest_framework.views import APIView
from rest_framework.response import Response
from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.google import views as google_view
from django.db import transaction
from api.serializers.auth.auth_serializers import OAuthGoogleRegisterSerializer
from website.models import Profile, Department
import json, requests

state = settings.STATE
client_id = settings.SOCIAL_AUTH_GOOGLE_CLIENT_ID
client_secret = settings.SOCIAL_AUTH_GOOGLE_SECRET
BASE_URL = "http://127.0.0.1:2424/"
GOOGLE_CALLBACK_URI = BASE_URL + "api/oauth/google/login/callback/"

class OAuthGoogleLoginView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, *args, **kwargs):
        scope = "https://www.googleapis.com/auth/userinfo.email"
        return redirect(f"https://accounts.google.com/o/oauth2/v2/auth?client_id={client_id}&response_type=code&redirect_uri={GOOGLE_CALLBACK_URI}&scope={scope}")



class OAuthGoogleCallbackView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, *args, **kwargs):
        access_token = request.GET.get("accessToken", "")
        code = request.GET.get("code", "")
        if not access_token:
            token_req = requests.post(f"https://oauth2.googleapis.com/token?client_id={client_id}&client_secret={client_secret}&code={code}&grant_type=authorization_code&redirect_uri={GOOGLE_CALLBACK_URI}&state={state}")
            token_req_json = token_req.json()
            error = token_req_json.get("error")
            if error is not None:
                raise json.JSONDecodeError(error)
            access_token =token_req_json.get("access_token")

        user_info_req = requests.get(f"https://www.googleapis.com/oauth2/v3/userinfo?access_token={access_token}")
        # email_req = requests.get(f"https://www.googleapis.com/oauth2/v1/tokeninfo?access_token={access_token}")

        user_info = user_info_req.json()
        email = user_info.get("email")

        try:
            user = User.objects.get(email = email, username=email)
        except:
            return Response({"message" : "가입된 사용자가 아닙니다."}, status=status.HTTP_400_BAD_REQUEST)

        if user.profile.reg_root == "workday":
            return Response({"message" : "Workday 계정으로 가입된 사용자 입니다."}, status=status.HTTP_400_BAD_REQUEST)

        url = "http://127.0.0.1:2424/api/login/"
        headers = {'Content-Type': 'application/json', 'charset': 'UTF-8', 'Accept': '*/*'}
        data = json.dumps({"email": user.email, "password": "None", "login_type" : "google"})
        login_req = requests.post(url=url, headers=headers, data=data)
        result = login_req.json()

        if login_req.status_code != 200:
            return Response({"message" : result.get("message", "로그인 실패..")}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(result, status=status.HTTP_200_OK)


class CheckGoogleUserView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, *args, **kwargs):
        access_token = request.GET.get("accessToken", "")
        if not access_token:
            return Response({"message" : "access_token을 입력해주세요"}, status=status.HTTP_400_BAD_REQUEST)
        
        user_info_req = requests.get(f"https://www.googleapis.com/oauth2/v3/userinfo?access_token={access_token}")

        if user_info_req.status_code != 200:
            return Response({"message" : "잘못된 access_token 입니다."}, status=status.HTTP_400_BAD_REQUEST)

        user_info = user_info_req.json()
        email = user_info.get("email", "")
        try:
            user = User.objects.get(email=email, username = email)
        except:
            return Response({"reg_flag" : False}, status=status.HTTP_200_OK)

        return Response({"reg_flag" : True}, status=status.HTTP_200_OK)


class OAuthGoogleRegisterView(GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = OAuthGoogleRegisterSerializer
    def post(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                membername = serializer.validated_data["membername"]
                department_id = serializer.validated_data["image"]
                access_token = serializer.validated_data["accessToken"]

                if not access_token:
                    return Response({"message" : "access_token을 입력해주세요"}, status=status.HTTP_400_BAD_REQUEST)
                
                user_info_req = requests.get(f"https://www.googleapis.com/oauth2/v3/userinfo?access_token={access_token}")

                if user_info_req.status_code != 200:
                    return Response({"message" : "잘못된 access_token 입니다."}, status=status.HTTP_400_BAD_REQUEST)

                user_info = user_info_req.json()
                email = user_info.get("email", "")
                image = user_info.get("picture", "")

                if User.objects.filter(email=email).exists():
                    return Response({"message" : "이미 가입된 사용자 입니다."}, status=status.HTTP_400_BAD_REQUEST)

                department = Department.objects.get(id = department_id)

                user = User.objects.create_user(username=email, email=email, last_name=membername)
                user.profile.image = image
                user.profile.reg_root = "google"
                user.profile.check_flag = "0"
                user.profile.department = department
                user.save()

        except:
            return Response({"message" : "가입 실패"}, status=status.HTTP_400_BAD_REQUEST)
            
        url = "http://127.0.0.1:2424/api/login/"
        headers = {'Content-Type': 'application/json', 'charset': 'UTF-8', 'Accept': '*/*'}
        data = json.dumps({"email": user.email, "password": "None", "login_type" : "google"})
        login_req = requests.post(url=url, headers=headers, data=data)
        result = login_req.json()

        if login_req.status_code != 200:
            return Response({"message" : result.get("message", "로그인 실패..")}, status=status.HTTP_400_BAD_REQUEST)

        return Response(result, status=status.HTTP_202_ACCEPTED)





