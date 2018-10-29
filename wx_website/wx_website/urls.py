"""wx_website URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from apps.expense import views


urlpatterns = [
    url(r'^$', views.web_root_index),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^expense/', include('apps.expense.urls', namespace="expense")),
    url(r'^wxmp/', include('apps.wxmp.urls', namespace="wxmp")),
    url(r'^gohome/', include('apps.gohome.urls', namespace="gohome")),
    url(r'^happytea/', include('apps.happytea.urls', namespace="happytea")),
    url(r'^happytea_wxapp/', include('apps.happytea_wxapp.urls', namespace="happytea_wxapp")),
    url(r'^ims/', include('apps.ims.urls', namespace="ims")),
    url(r'^hcp/', include('apps.hcp.urls', namespace="hcp")),
    url(r'^mail_proxy/', include('apps.mail_proxy.urls', namespace="mail_proxy")),
]
