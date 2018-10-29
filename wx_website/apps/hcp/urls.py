
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^ims_list/([0-9]*)/$', views.ims_list, name='info_list'),
    url(r'^ims_rpt/([0-9]*)/$', views.ims_rpt, name='rpt'),
    url(r'^ims_detail/([0-9]*)/$', views.ims_detail, name='detail'),
    url(r'^ims_login/([a-z]*)/$', views.ims_login, name='login2'),
    url(r'^ajax_get_list/([0-9]*)/$', views.ajax_get_list, name='ajax_get_list'),
    url(r'^do_login/$', views.do_login, name='do_login'),
    url(r'^ims_new/$', views.ims_new, name='ims_new'),
    url(r'^ims_about/$', views.ims_about, name='ims_about'),
    url(r'^ims_logout/$', views.ims_logout, name='ims_logout'),
    url(r'^$', views.ims_list, name='index'),
]
