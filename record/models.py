from django.db import models

# Create your models here.
from django.utils.html import format_html


class Record(models.Model):
    record_url = models.CharField(max_length=100)
    datetime = models.DateField(null=True,verbose_name='监控日期')

    def __str__(self):
        return "<Record:({record_url},{datetime})>".format(record_url = self.record_url,datetime = self.datetime)

    def video_url(self):
        return format_html(
            '<video width="320" height="240" controls src="/{}" id="{}" class="thisVideo">',
                self.record_url,
                self.id,
            '<p>您的浏览器不支持视频播放</p>'
            '</video>',

        )
    video_url.short_description=u'监控视频'

class Recording(models.Model):
    pass