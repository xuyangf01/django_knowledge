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
from django.urls import path, re_path
from apps.show_idea.views import Index, QctObjectDetail, QctListShow, SctListShow, MyChangePwd

urlpatterns = [
    re_path(r'^index/$', Index.as_view(), name='index'),
    path('change_pwd/', MyChangePwd.as_view(), name='pwd_change'),
    path('s_list/<int:t_id>/', SctListShow.as_view(), name="sct_list"),
    path('q_list/<int:t_id>/', QctListShow.as_view(), name="qct_list"),
    path('q_datail/<int:t_id>/', QctObjectDetail.as_view(), name="qct_detail"),
]
