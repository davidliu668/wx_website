# coding=utf-8
from django.shortcuts import render
from models import *


def account_list(request):
    act_list = Account.objects.order_by('name')
    context = {'account_list': act_list}
    return render(request, 'gohome/account_list.html', context)


def account_info(request):
    pass


def account_edit(request):
    pass


def account_imports(request):
    pass
