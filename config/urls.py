from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

from drf_spectacular.views import SpectacularJSONAPIView
from drf_spectacular.views import SpectacularRedocView
from drf_spectacular.views import SpectacularSwaggerView
from drf_spectacular.views import SpectacularYAMLAPIView


urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('', include("website.urls")),
    path('api/', include("api.urls")),
    path('oauth/', include("allauth.urls")),
    path('summernote/', include('django_summernote.urls')),

    # Open API 자체를 조회 : json, yaml, 
    path("docs/json/", SpectacularJSONAPIView.as_view(), name="schema-json"),
    path("docs/yaml/", SpectacularYAMLAPIView.as_view(), name="swagger-yaml"),
    # Open API Document UI로 조회: Swagger, Redoc
    path("docs/swagger/", SpectacularSwaggerView.as_view(url_name="schema-json"), name="swagger-ui",),
    path("docs/redoc/", SpectacularRedocView.as_view(url_name="schema-json"), name="redoc",),

] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
