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
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path(r'', include(('main.urls', 'main'), namespace='main')),
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



admin.site.site_header = 'TipArticle.com Administrator@Pius_Lucky'
admin.site.site_title = 'TipArticle.com Administrator@Pius_Lucky'

