from django.contrib import admin
from .models import ReadNum, ReadingDetail


@admin.register(ReadNum)
class ReadNumAdmin(admin.ModelAdmin):
    list_display = ('read_num', 'content_type')


@admin.register(ReadingDetail)
class ReadDetailAdmin(admin.ModelAdmin):
    list_display = ('date', 'read_num', 'content_type')
