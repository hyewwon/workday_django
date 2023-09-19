from django.urls import path
from oauth.views.oauth_google_views import google_login, google_callback

app_name = "oauth"

urlpatterns = [
    path("google/login/", google_login, name="google_login"),
    path("google/callback/", google_callback, name="google_callback"),
    # path("google/login/finish/", GoogleLoginView.as_view(), name="google_login_finish"),
]
