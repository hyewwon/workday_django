from django.views.generic import View
from django.conf import settings
from django.shortcuts import render,  redirect
from django.http import HttpRequest, JsonResponse
from django.contrib.auth.models import User
from django.db import transaction
from django.contrib import messages
from website.models import Profile, Company, Department
import json, requests, jwt

state = settings.STATE
client_id = settings.SOCIAL_AUTH_GOOGLE_CLIENT_ID
client_secret = settings.SOCIAL_AUTH_GOOGLE_SECRET
BASE_URL = "http://127.0.0.1:2424/"
GOOGLE_CALLBACK_URI = BASE_URL + "google/login/callback/"

class OAuthGoogleLoginView(View):
    def get(self, request:HttpRequest, *args, **kwargs):
        scope = "https://www.googleapis.com/auth/userinfo.email"
        return redirect(f"https://accounts.google.com/o/oauth2/v2/auth?client_id={client_id}&response_type=code&redirect_uri={GOOGLE_CALLBACK_URI}&scope={scope}")


class OAuthGoogleCallbackView(View):
    '''
        구글 계정 로그인
    '''
    def get(self, request:HttpRequest, *args, **kwargs):
        context = {}
        code = request.GET.get("code", "")
        token_req = requests.post(f"https://oauth2.googleapis.com/token?client_id={client_id}&client_secret={client_secret}&code={code}&grant_type=authorization_code&redirect_uri={GOOGLE_CALLBACK_URI}&state={state}")
        token_req_json = token_req.json()
        error = token_req_json.get("error")
        if error is not None:
            raise json.JSONDecodeError(error)
        access_token =token_req_json.get("access_token")

        user_info_req = requests.get(f"https://www.googleapis.com/oauth2/v3/userinfo?access_token={access_token}")
        # email_req = requests.get(f"https://www.googleapis.com/oauth2/v1/tokeninfo?access_token={access_token}")

        if user_info_req.status_code != 200:
            messages.warning(request, "엑세스 토큰 에러..")
            return redirect("/login/")

        user_info = user_info_req.json()
        email = user_info.get("email")
        image = user_info.get("picture", "")

        try:
            user = User.objects.get(email = email, username=email)
        except:
            with transaction.atomic():
                user = User.objects.create_user(username=email, email=email)
                user.profile.image = image
                user.profile.reg_root = "google"
                user.profile.check_flag = "0"
                user.save()
            
            return redirect(f"/google-register/?access_token={access_token}")
        
        try:
            if not user.profile.department:
                return redirect(f"/google-register/?access_token={access_token}")

            if user.profile.reg_root == "workday":
                messages.warning(request, "workday에 등록된 이메일 입니다.")
                return render("/login/")

            url = "http://127.0.0.1:2424/api/login/"
            headers = {'Content-Type': 'application/json', 'charset': 'UTF-8', 'Accept': '*/*'}
            data = json.dumps({"email": user.email, "password": "None", "login_type" : "google"})
            login_req = requests.post(url=url, headers=headers, data=data)
            result = login_req.json()
            
            if login_req.status_code != 200:
                messages.warning(request, result.get("message"))
                return redirect("/login/")

            response = redirect("/")
            response.set_cookie("access_token", result["jwt_token"]["access_token"], max_age=int(60 * 20))
            response.set_cookie("refresh_token_index_id", result["jwt_token"]["refresh_token_index_id"], max_age=result["jwt_token"]["refresh_token_exp"])
            return response
        
        except Exception as e:
            print(e)
            response = redirect("/")
            return response



class GoogleRegisterView(View):
    '''
        구글 계정 회원가입
    '''
    def get(self, request:HttpRequest, *args, **kwargs):
        context = {}
        access_token = request.GET.get("access_token", "")
        if not access_token:
            messages.warning(request, "토큰 에러..")
            return redirect("/login/")
        companys = Company.objects.all()
        context["companys"] = companys
        context["access_token"] = access_token
        
        return render(request, "auth/google_register.html", context)
    
    def post(self, request:HttpRequest, *args, **kwargs):
        context = {}
        access_token = request.POST.get("access_token", "")
        membername = request.POST.get("membername", "")
        department_id = request.POST.get("department_id", "")

        user_info_req = requests.get(f"https://www.googleapis.com/oauth2/v3/userinfo?access_token={access_token}")
        if user_info_req.status_code != 200:
            context["success"] = False
            context["message"] = "유저 토큰 정보 에러"
            return JsonResponse(context, content_type="application/json")

        user_info = user_info_req.json()
        email = user_info.get("email")

        try:
            user = User.objects.get(email = email, username=email)
            department = Department.objects.get(id = department_id)

            if user.profile.reg_root == "workday":
                return render("/login/")

            with transaction.atomic():
                user.last_name = membername
                user.profile.department = department
                user.save()

        except: 
            context["success"] = False
            context["message"] = "신청 에러.."
            return JsonResponse(context, content_type="application/json")

        context["success"] = True
        context["message"] = "신청되었습니다"
        return JsonResponse(context, content_type="application/json")




        


