from django.views.generic import View
from django.http import HttpRequest
from django.shortcuts import render
from django.utils.decorators import method_decorator
from website.utils import getTokenUser
from website.decorators import login_required
from website.models import Vacation, Department, Profile

class VacationViews(View):
    @method_decorator(login_required(redirect_url="website:login"))
    def get(self, request: HttpRequest, *args, **kwargs):
        context = {}
        access_token = request.COOKIES.get("access_token", None)
        user = getTokenUser(token=access_token)
        user_department = Profile.objects.get(user__id = user.id).department.id
        department = Department.objects.all()
        user_vacation = Vacation.objects.filter(user = user).order_by("start_date")

        context["user"] = user
        context["department"] = department
        context["user_department"] = user_department
        context["user_vacation"] = user_vacation

        return render(request,"attendance/vacation.html", context)
