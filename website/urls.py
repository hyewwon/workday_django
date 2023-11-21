from django.urls import path
from website.views.auth_views.auth_views import HomeView, RegisterView, LoginView
from website.views.mypage_views.mypage_views import MyPageView, MyPageEditView
from website.views.attendance_views.vacation_views import VacationViews
from website.views.attendance_views.attendance_views import AttendanceView
from website.views.notice_views.notice_views import NoticeView
from website.views.free_board_views.free_board_views import FreeBoradView, FreeBoardCreateView, FreeBoardDetailView
from website.views.auth_views.oauth_google_views import OAuthGoogleCallbackView, OAuthGoogleLoginView


app_name = "website"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("login/", LoginView.as_view(), name="login"),
    path("register/", RegisterView.as_view(), name="register"),

    path("mypage/", MyPageView.as_view(), name="mypage"),
    path("mypage-edit/", MyPageEditView.as_view(), name="mypage_edit"),

    path("attendance/",AttendanceView.as_view(), name="attendance"),
    path("vacation/", VacationViews.as_view(), name="vacation"),

    path("noice/",NoticeView.as_view(), name="notice"),
    path("free-borad/",FreeBoradView.as_view(), name="free_board"),
    path("free-borad-create/",FreeBoardCreateView.as_view(), name="free_board_create"),
    path("free-borad-detail/<int:pk>/",FreeBoardDetailView.as_view(), name="free_board_detail"),

    path("google/login/", OAuthGoogleLoginView.as_view(), name="google_login"),
    path("google/login/callback/", OAuthGoogleCallbackView.as_view(), name="google_callback"),
]
