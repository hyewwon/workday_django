from django.views.generic import View
from django.http import HttpRequest
from django.shortcuts import render
from django.utils.decorators import method_decorator
from website.decorators import login_required
from website.utils import getTokenUser
from website.models import Department

class MyPageView(View):
    @method_decorator(login_required(redirect_url="website:login"))
    def get(self, request: HttpRequest, *args, **kwargs):
        context = {}
        access_token = request.COOKIES.get("access_token", None)
        user = getTokenUser(token=access_token)
        context["user"] = user
        return render(request, "mypage/mypage.html", context)


class MyPageEditView(View):
    @method_decorator(login_required(redirect_url="website:login"))
    def get(self, request: HttpRequest, *args, **kwargs):
        context = {}
        access_token = request.COOKIES.get("access_token", None)
        user = getTokenUser(token=access_token)

        department = Department.objects.all().values("name")
        context["user"] = user
        context["department"] = department

        return render(request, "mypage/mypage_edit.html", context)
