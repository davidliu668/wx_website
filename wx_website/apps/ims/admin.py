# coding=utf-8
from django.contrib import admin
from .models import *


@admin.register(MColName)
class MColNameAdmin(admin.ModelAdmin):
    list_display = ('id', 'col_index', 'col_name', )
    search_fields = ('id', 'col_index', 'col_name',)
    ordering = ('col_index',)


@admin.register(MInfo)
class MInfoAdmin(admin.ModelAdmin):
    list_display = ('id', 'f01', 'f02', 'f03', 'f04', 'f05', )
    search_fields = ('id', 'f01', 'f02', 'f03', 'f04', 'f05', )
    ordering = ('-id',)


@admin.register(MUser)
class MUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'passwd', )
    search_fields = ('id', 'name', 'passwd', )
    ordering = ('-id',)
