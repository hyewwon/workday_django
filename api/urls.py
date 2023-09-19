from django.urls import path
from rest_framework_simplejwt.views import TokenVerifyView
from api.views.auth_views.auth_views import CheckUsernameView, CheckEmailView, RegisterView, LoginView, ReissueTokenView, LogoutView
from api.views.mypage_views.mypage_veiws import MyPageEditView, MyPageEditPasswordView
from api.views.attendance_views.vacation_views import VacationView, VacationDeleteView
from api.views.attendance_views.attendance_views import AttendanceView
from api.views.free_board_views.free_board_views import FreeBoardCreateView, FreeBoardDetailView

app_name = "api"

urlpatterns = [
    path("check-username/", CheckUsernameView.as_view(), name="check_username"),
    path("check-email/", CheckEmailView.as_view(), name="check_email"),
    path("registration/", RegisterView.as_view(), name="registration"),

    path("login/", LoginView.as_view(), name="login"),
    path("token/verify/", TokenVerifyView.as_view()),
    path("token/refresh/", ReissueTokenView.as_view()),
    path("token/refresh/", ReissueTokenView.as_view()),
    path("logout/", LogoutView.as_view(), name="logout"),

    path("mypage-edit/", MyPageEditView.as_view(), name="mypage_edit"),
    path("mypage-password-edit/", MyPageEditPasswordView.as_view(), name="mypage_edit"),

    path("attendance/", AttendanceView.as_view(), name="attendance"),
    path("vacation/", VacationView.as_view(), name="vacation"),
    path("vacation-delete/", VacationDeleteView.as_view(), name="vacation_delete"),

    path("free-board-create/", FreeBoardCreateView.as_view(), name="free_board_create"),
    path("free-board-detail/<int:pk>/", FreeBoardDetailView.as_view(), name="free_board_detail"),


]
