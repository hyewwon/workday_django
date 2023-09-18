from django.conf import settings
from django.contrib.auth.models import User
from allauth.socialaccount.models import SocialAccount
from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from django.http import JsonResponse
from rest_framework import status
from json.decoder import JSONDecodeError

state = settings.STATE
BASE_URL = "http://127.0.0.1:2424/"
GOOGLE_CALLBACK_URI = BASE_URL + "accounts/google/callback/"
