from django.views.generic import View
from django.http import HttpRequest
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.db.models import Q, Case, When, Value, F, Prefetch, Subquery, OuterRef
from website.utils import getTokenUser
from website.decorators import login_required
from website.models import Attendance
from django.utils import timezone
from django.conf import settings
import json, requests

class AttendanceView(View):
    @method_decorator(login_required(redirect_url="website:login"))
    def get(self, request, *args, **kwargs):
        context = {}
        access_token = request.COOKIES.get("access_token", None)
        user = getTokenUser(token=access_token)
        today = timezone.now().date()
        attendance = Attendance.objects.filter(user = user).order_by("-created_at")

        context["user"] = user
        context["today_flag"] = len(attendance) >= 1 and str(attendance.last().created_at).split(" ")[0] == str(today)
        context["attendance"] = attendance if context["today_flag"] else attendance[:len(attendance)-1]

        return render(request, "attendance/attendance.html", context)


# 현재 위도 경도 
def get_latitude_longitude():
    api_key = settings.IP_API_KEY
    url = "http://api.ipstack.com/check?access_key=" + api_key
    result = json.loads(requests.get(url).text)
    latitude = result["latitude"]
    longitude = result["longitude"]

    return latitude, longitude