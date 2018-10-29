from django.contrib import admin

from models import TeaCharge
from models import User
from models import Team

# Register your models here.


class TeaChargeAdmin(admin.ModelAdmin):
    list_display = ('id', 'team_id', 'user_id', 'money', 'charge_time', 'create_time', 'expense', 'add_type')
    list_filter = ('team_id', 'user_id', 'add_type')
    search_fields = ('team_id', 'user_id', 'charge_time')
    ordering = ('-charge_time',)


admin.site.register(TeaCharge, TeaChargeAdmin)


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'rtx', 'team_id', 'status', 'is_admin', 'openid')
    list_filter = ('team_id', 'status')
    search_fields = ('rtx')
    ordering = ('id',)


admin.site.register(User, UserAdmin)


class TeamAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    ordering = ('id',)


admin.site.register(Team, TeamAdmin)
