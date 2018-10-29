
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^ims_list/$', views.ims_list, name='info_list'),
    url(r'^ims_detail/([0-9]*)/$', views.ims_detail, name='detail'),
    url(r'^ims_login/([a-z]*)/$', views.ims_login, name='login'),
    url(r'^ajax_get_list/$', views.ajax_get_list, name='ajax_get_list'),
    url(r'^do_login/$', views.do_login, name='do_login'),
    url(r'^view_log/$', views.view_log, name='view_log'),
    url(r'^$', views.ims_list, name='index'),
]
