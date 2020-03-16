"""img_base64_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path(' ', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path, re_path, include
from rest_framework.documentation import include_docs_urls
from rest_framework.schemas import get_schema_view
from rest_framework_swagger.views import get_swagger_view # new
from rest_framework_simplejwt import views as jwt_views
from allauth.account.views import confirm_email
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


API_TITLE = 'ImageBase64 API'
API_DESCRIPTION = 'A Web API for encoding image to Base64 string and decoding any base64 string back to image.'
API_VERSION = 'v1.0.0'
schema_view = get_schema_view(
openapi.Info(
title= API_TITLE,
default_version=API_VERSION,
description= API_DESCRIPTION,
contact=openapi.Contact(email="luckypius50@gmail.com"),
),
public=True,
permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path(r'', include(('main.urls', 'main'), namespace='main')),
    path('api/v1/', include('api.urls')), 
    path('api-auth/', include('rest_framework.urls')),
    path('api/v1/rest-auth/', include('rest_auth.urls')),
    path('api/v1/rest-auth/registration/', include('rest_auth.registration.urls')),
    re_path(r"^rest-auth/registration/account-confirm-email/(?P<key>[\s\d\w().+-_',:&]+)/$", confirm_email,
        name="account_confirm_email"),
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

]

if settings.DEBUG or not settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # Customized by Lucky_P (I try as much as possible to prevent files conflict)
    urlpatterns += static(settings.FILE_URL, document_root=settings.FILE_ROOT)
    urlpatterns += static(settings.PASTE_URL, document_root=settings.PASTE_ROOT)
    urlpatterns += static(settings.LINK_URL, document_root=settings.LINK_ROOT)
    urlpatterns += static(settings.ENCODE_URL, document_root=settings.ENCODE_ROOT)
    # for front-end.
    urlpatterns += static(settings.FRONTEND_URL, document_root=settings.FRONTEND_ROOT)



admin.site.site_header = 'ImageBase64 Administrator@Pius_Lucky'
admin.site.site_title = 'ImageBase64 Administrator@Pius_Lucky'
