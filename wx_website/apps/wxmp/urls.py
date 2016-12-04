
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.wx_msg_dispatch, name='wx_msg_dispatch'),
    url(r'^debug$', views.wx_debug, name='wx_debug'),
]
