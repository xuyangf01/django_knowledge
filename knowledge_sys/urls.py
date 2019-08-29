"""knowledge_sys URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.static import serve
from django.conf import settings
from show_idea.views import Index, page_not_found, LoginKnowledge, account_logout

urlpatterns = [
    path('management/', admin.site.urls),
    re_path(r'^$', Index.as_view(), name="site_index"),
    re_path(r'login/$', LoginKnowledge.as_view(), name="login"),
    re_path(r'^logout/$', account_logout, name="logout"),
    re_path(r'show/', include(("show_idea.urls", 'show_idea'), namespace='show_idea')),
    re_path(r'ckeditor/', include('ckeditor_uploader.urls')),
    re_path(r'^media/(?P<path>.*)$', serve, {"document_root": settings.MEDIA_ROOT}),
    re_path(r'search/', include('haystack.urls')),
]

handler404 = page_not_found
LOGIN_URL = '/login/'