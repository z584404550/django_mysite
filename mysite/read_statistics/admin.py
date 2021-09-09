from django.contrib import admin
from .models import ReadNum, ReadDetail

# Register your models here.


@admin.register(ReadNum)
class BlogNumAdmin(admin.ModelAdmin):
    list_display = ('read_num', 'content_object')


@admin.register(ReadDetail)
class BlogNumAdmin(admin.ModelAdmin):
    list_display = ('date', 'read_num', 'content_object')