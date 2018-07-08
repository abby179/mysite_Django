from django.contrib import admin
from .models import LikeRecord


@admin.register(LikeRecord)
class LikeRecordAdmin(admin.ModelAdmin):
    list_display = ('content_object', 'liked_time', 'user')
