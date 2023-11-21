from django.views.generic import View
from django.conf import settings
from django.shortcuts import render,  redirect
from django.http import HttpRequest
from django.contrib.auth.models import User
from allauth.socialaccount.models import SocialAccount, SocialApp
from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.google import views as google_view
from django.db import transaction
from website.models import Profile
import json, requests

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

        user_info = user_info_req.json()
        email = user_info.get("email")
        given_name = user_info.get("given_name", "")
        family_name = user_info.get("family_name", "")
        nickname = user_info.get("nickname", "")
        name = user_info.get("name", "")
        image = user_info.get("picture", "")

        try:
            user = User.objects.get(email = email, username=email)
        except:
            with transaction.atomic():
                last_name = name or given_name+family_name
                user = User.objects.create_user(username=email, email=email, last_name=last_name)
                user.profile.image = image
                user.profile.reg_root = "google"
                user.profile.check_flag = "0"
                user.save()

        if user.profile.reg_root == "workday":

            return render(request, "auth/login.html")

        url = "http://127.0.0.1:2424/api/login/"
        headers = {'Content-Type': 'application/json', 'charset': 'UTF-8', 'Accept': '*/*'}
        data = json.dumps({"email": user.email, "password": "None", "login_type" : "google"})
        login_req = requests.post(url=url, headers=headers, data=data)
        result = login_req.json()

        if login_req.status_code != 200:
            return redirect("/login/", kwargs={"message": "hi"})
        
        return redirect("/")