from django.contrib import admin

from models import expense_list

# Register your models here.


class ExpenseListAdmin(admin.ModelAdmin):
    list_display = ('time', 'money', 'remark')
    list_filter = ('time', 'money')
    search_fields = ('time', 'money', 'remark')
    ording = ('-time',)


admin.site.register(expense_list, ExpenseListAdmin)
