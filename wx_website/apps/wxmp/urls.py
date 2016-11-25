
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.wx_reg, name='wx_reg'),
    url(r'^debug$', views.wx_debug, name='wx_debug'),
]
