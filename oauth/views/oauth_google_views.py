from django.conf import settings
from django.shortcuts import render,  redirect
from django.contrib.auth.models import User
from allauth.socialaccount.models import SocialAccount
from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from django.http import JsonResponse
from rest_framework import status
from rest_framework.generics import GenericAPIView
from json.decoder import JSONDecodeError
import os, requests

state = settings.STATE
client_id = settings.SOCIAL_AUTH_GOOGLE_CLIENT_ID
client_secret = settings.SOCIAL_AUTH_GOOGLE_SECRET
BASE_URL = "http://127.0.0.1:2424/"
GOOGLE_CALLBACK_URI = BASE_URL + "oauth/google/callback/"

def google_login(request):
    print(GOOGLE_CALLBACK_URI, "===================================")
    scope = "https://www.googleapis.com/auth/userinfo.email"
    return redirect(f"https://accounts.google.com/o/oauth2/v2/auth?client_id={client_id}&response_type=code&redirect_uri={GOOGLE_CALLBACK_URI}&scope={scope}")


def google_callback(request):
    code = request.GET.get('code')
    token_req = requests.post(
        f"https://oauth2.googleapis.com/token?client_id={client_id}&client_secret={client_secret}&code={code}&grant_type=authorization_code&redirect_uri={GOOGLE_CALLBACK_URI}&state={state}")
    token_req_json = token_req.json()
    error = token_req_json.get("error")
    if error is not None:
        raise JSONDecodeError(error)
    access_token = token_req_json.get('access_token')

    print(access_token)
    return

class GoogleLoginView(GenericAPIView):
    
    def get(self, request, *args, **kwargs):
        scope = "https://www.googleapis.com/auth/userinfo.email"
        return redirect(f"https://accounts.google.com/o/oauth2/v2/auth?client_id={client_id}&response_type=code&redirect_uri={GOOGLE_CALLBACK_URI}&scope={scope}")