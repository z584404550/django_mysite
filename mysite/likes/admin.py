from django.contrib import admin
from .models import LikeCount, LikeRecord

# Register your models here.


@admin.register(LikeCount)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('content_object', 'like_num')


@admin.register(LikeRecord)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('content_object', 'user')
