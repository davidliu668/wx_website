from django.contrib import admin
from models import AppUser

# Register your models here.


class AppUserAdmin(admin.ModelAdmin):
    list_display = ('app_openid', 'user_id', 'nickname', 'bind_time')
    search_fields = ('app_openid', 'user_id', 'nickname')
    ordering = ('-bind_time',)


admin.site.register(AppUser, AppUserAdmin)
