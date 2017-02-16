from django.contrib import admin
from models import Account

# Register your models here.


class AccountAdmin(admin.ModelAdmin):
    list_display = ('from_station', 'end_station', 'start_date',
                    'end_date', 'name', 'passwd', 'status')
    list_filter = ('status', 'from_station')
    search_fields = ('from_station', 'start_date', 'end_station', 'name')
    ordering = ('from_station', 'name')


admin.site.register(Account, AccountAdmin)
