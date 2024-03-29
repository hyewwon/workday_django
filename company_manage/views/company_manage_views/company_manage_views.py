from django.views.generic import View, TemplateView
from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from website.decorators import login_required
from website.utils import getTokenUser
from website.models import Department, Company
import requests, json

class HomeView(TemplateView):
    template_name = "company_manage/home.html"
    @method_decorator(login_required(redirect_url="website:login"))
    def get(self, request:HttpRequest, *args, **kwargs):
        context= {}
        access_token = request.COOKIES.get("access_token", None)
        user = getTokenUser(token=access_token)
        context["user"] = user
        return render(request, self.template_name, context)