from django.contrib import admin
from models import *

# Register your models here.


class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'from_station', 'to_station', 'time',
                    'name', 'sfz_id', 'remark', 'remark2', 'create_time')
    list_filter = ('user', 'from_station', 'time', 'create_time',)
    search_fields = ('user', 'from_station', 'to_station', 'time',
                     'name', 'sfz_id', 'remark', 'remark2')
    ordering = ('-create_time',)


admin.site.register(Order, OrderAdmin)


class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'wx_name', 'passwd',)
    search_fields = ('name', 'wx_name', 'passwd',)
    ordering = ('-create_time',)


admin.site.register(User, UserAdmin)
