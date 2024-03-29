from django.urls import path
from company_manage.views.company_manage_views.company_manage_views import HomeView
from company_manage.views.human_resource_manage_view.employee_manage_views import EmployeeManageView, RankByDepartmentView

app_name = "company_manage"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("rank-list/", RankByDepartmentView.as_view()),

    path("hr-manage/employee-manage/", EmployeeManageView.as_view(), name="employee_manage"),
]
