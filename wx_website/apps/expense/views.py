from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from models import expense_list

# Create your views here.

def index(request):
    latest_expense_list = expense_list.objects.order_by('-time')[:5]
    context = {'latest_expense_list': latest_expense_list}
    return render(request, 'expense/index.html', context)

def detail(request, expense_id):
    expense = get_object_or_404(expense_list, pk=expense_id)
    return render(request, 'expense/detail.html', {'expense': expense} )


