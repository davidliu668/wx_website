from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^la/get_openid', views.get_openid, name='get_openid'),
    url(r'^la/get_teachage_info', views.get_teachage_info, name='get_teachage_info'),
    url(r'^la/add_one_teacharge', views.add_one_teacharge, name='add_one_teacharge'),
    url(r'^la/get_activeinfo', views.get_activeinfo, name='get_activeinfo')
]
