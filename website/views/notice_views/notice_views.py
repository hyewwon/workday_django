from django.views.generic import View
from django.http import HttpRequest
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.db.models import Q, Case, When, Value, F, Prefetch, Subquery, OuterRef
from website.utils import getTokenUser
from website.decorators import login_required
from website.models import Attendance
from django.utils import timezone

class NoticeView(View):
    @method_decorator(login_required(redirect_url="website:login"))
    def get(self, request,*args, **kwargs):
        context = {}
        access_token = request.COOKIES.get("access_token", None)
        user = getTokenUser(token = access_token)
        context["user"] = user
        return render(request, "notice/notice.html", context)