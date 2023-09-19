from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('', include("website.urls")),
    path('api/', include("api.urls")),
    path('oauth/', include("allauth.urls")),
    path('oauth/', include("dj_rest_auth.urls")),
    path('oauth/', include("oauth.urls")),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
