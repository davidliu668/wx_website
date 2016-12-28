from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<expense_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^add/(?P<expense_id>[0-9]+)/$', views.add, name='add'),
    url(r'^del/(?P<expense_id>[0-9]+)/$', views.del_expense, name='del_expense'),
]
