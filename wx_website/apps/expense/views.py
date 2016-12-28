from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from models import expense_list
from models import exp_pic
from qcloud_cos import CosClient
from qcloud_cos import UploadFileRequest
import logging
import datetime
import os
import uuid
import hashlib

# Create your views here.
logger = logging.getLogger(__name__)

# cos config
cos_appid = 1251650800               
cos_secret_id = u'AKIDUYWJuJwbS7cv3zoQq6C6A4nKfsqdhMmE'        
cos_secret_key = u'fPJ5rz2tY3azFOOPRsMqKpKoiYNDIKfy'        
cos_region = "guangzhou"


def index(request):
    latest_expense_list = expense_list.objects.order_by('-time')
    context = {'latest_expense_list': latest_expense_list}
    return render(request, 'expense/index.html', context)


def detail(request, expense_id):
    exp_pic_url = "#"
    if expense_id == "0":
        expense = expense_list(pk=0, money=0, time=datetime.datetime.now(), remark='')
    else:
        expense = get_object_or_404(expense_list, pk=expense_id)

        # get the cos_access_url for exp_pic
        if expense.fileid != 0:
            exp_pic_obj = exp_pic.objects.get(pk=expense.fileid)
            exp_pic_url = exp_pic_obj.access_url

    return render(request, 'expense/detail.html', {'expense': expense, "exp_pic_url": exp_pic_url})


def del_expense(request, expense_id):
    expense = get_object_or_404(expense_list, pk=expense_id)
    expense.delete()
    return HttpResponseRedirect('/expense/')


def add(request, expense_id):
    expense_id = int(expense_id)

    input_date = request.POST['input_date']
    input_money = request.POST['input_money']
    input_remark = request.POST['input_remark']
    input_is_expense = request.POST['input_is_expense']
    input_file =request.FILES.get('input_file', None)

    d_date = datetime.datetime.strptime(input_date, '%Y-%m-%d %H:%M:%S')
    d_money = float(input_money)
    d_remark = input_remark
    d_is_expense = (input_is_expense == '1')
    d_openid = ''

    d_fileid = 0
    if input_file is None:
        pass
    else:
        (_ret, filename, filepath, filemd5) = save_file(input_file)
        cos_client = CosClient(cos_appid, cos_secret_id, cos_secret_key, cos_region)
        cos_upload_req = UploadFileRequest(u'expense', u'/' + filename.decode('utf8'), filepath.decode('utf8'))
        cos_upload_req.set_insert_only(0)
        cos_upload_rsp = cos_client.upload_file(cos_upload_req)

        if cos_upload_rsp['code'] == 0:
            cos_uri = cos_upload_rsp['data']['url']
            access_url = cos_upload_rsp['data']['source_url']

            d_fileid = exp_pic.add(cos_uri, access_url, filemd5)
        else:
            logger.error('cos upload fail, msg:' + str(cos_upload_rsp))

        os.remove(filepath)

    if expense_id == 0:
        # add expense
        expense_list.add_expense(
            d_money, d_date, d_remark, d_is_expense, d_openid, d_fileid)

        return HttpResponseRedirect('/expense/')
    else:
        # update expense
        expense_obj = expense_list.objects.get(pk=expense_id)
        expense_obj.time = d_date
        expense_obj.money = d_money
        expense_obj.remark = d_remark
        expense_obj.is_expense = d_is_expense
        if input_file is not None:
            expense_obj.fileid = d_fileid
        expense_obj.save()

        return HttpResponseRedirect('/expense/')


def save_file(input_file):
    filename = str(uuid.uuid1())
    filepath = os.path.join('/tmp/expense', filename)
    fp = open(filepath, 'wb+')
    for chunk in input_file.chunks(): 
        fp.write(chunk)
    fp.close()

    fp = open(filepath, 'rb')
    md5obj = hashlib.md5()
    md5obj.update(fp.read())
    filemd5 = str(md5obj.hexdigest())
    fp.close()

    return (0, filename, filepath, filemd5)

