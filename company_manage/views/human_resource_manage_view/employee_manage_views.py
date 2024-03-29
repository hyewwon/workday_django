from django.views.generic import View, TemplateView
from django.http import HttpRequest, JsonResponse
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User
from website.decorators import login_required
from website.utils import getTokenUser
from website.models import Department, Company, Rank
import requests, json

class EmployeeManageView(View):
    '''
        인사 권한 관리
    '''
    @method_decorator(login_required(redirect_url="website:login"))
    def get(self, request:HttpRequest, *args, **kwargs):
        context= {}
        access_token = request.COOKIES.get("access_token", None)
        user = getTokenUser(token=access_token)
        context["user"] = user
        users = User.objects.all().values("last_name","date_joined", "profile__department__name", "profile__rank__name","email")
        context["user_data"] = users
        context["department"] = Department.objects.all().values("id", "name")

        return render(request, "human_resource_manage/employee_manage.html", context)
        


class RankByDepartmentView(View):
    '''
        부서별 직급 
    '''
    @method_decorator(login_required(redirect_url="website:login"))
    def get(self, request:HttpRequest, *args, **kwargs):
        context={}
        access_token = request.COOKIES.get("access_token", None)
        user = getTokenUser(token=access_token)
        context["user"] = user
        department_id = request.GET.get("id")
        try:
            department = Department.objects.get(id=department_id)
        except:
            return JsonResponse(context, content_type="application/json", status=400)
        
        rank = Rank.objects.filter(deparmtent=department).values("id", "name")
        context["rank"] = rank
        return JsonResponse(context, content_type="application/json", status=200)
