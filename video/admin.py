from django.contrib import admin

# Register your models here.
# from record import models
from video import models


@admin.register(models.Record)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('id','video_url','datetime')
