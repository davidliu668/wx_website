from django.contrib import admin

from models import appinfo
from models import token


# Register your models here.

class AppInfoAdmin(admin.ModelAdmin):
    list_display = ('wxid', 'appid', 'secret')
    search_fields = ('wxid', 'appid', 'secret')
    ordering = ('wxid',)


class Tokendmin(admin.ModelAdmin):
    list_display = ('wxid', 'token', 'time')
    search_fields = ('wxid', 'token', 'time')
    ordering = ('wxid',)


admin.site.register(appinfo, AppInfoAdmin)
admin.site.register(token, Tokendmin)
