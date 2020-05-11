from django.db import models

# Create your models here.
from django.utils.html import format_html


class Record(models.Model):
    record_url = models.CharField(max_length=100)
    datetime = models.DateField(null=True)

    # def __str__(self):
    #     return "<Record:({record_url},{datetime})>".format(record_url = self.record_url,datetime = self.datetime)

    def video_url(self):
        return format_html(
            '<video width="320" height="240" controls>'
                '<source src="/{}" type="video/avi">'
                '<object data="/{}" width="320" height="240">'
                    '<embed src="/{}" width="320" height="240">'
                '</object>'
            '</video>',
            self.record_url,
        )
    video_url.short_description=u'监控视频'