from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^account/$', views.account_list, name='account_list'),
    url(r'^account/(?P<expense_id>[0-9]+)/$', views.account_info, name='account_info'),
    url(r'^account/edit/(?P<expense_id>[0-9]+)/$', views.account_edit, name='account_edit'),
    url(r'^account/imports/$', views.account_imports, name='account_imports'),
]
