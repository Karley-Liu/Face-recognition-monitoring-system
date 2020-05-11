from django.db import models

# Create your models here.
from django.utils.html import format_html


class Faces(models.Model):
    face_url = models.CharField(verbose_name='人脸',max_length=100)
    face_date = models.DateField(verbose_name='提取人脸视频日期')

    def __str__(self):
        return "<Faces:({face_url},{face_date})>".format(face_url=self.face_url,face_date=self.face_date)

    def image_data(self):
        return format_html(
            '<img src="/{}" width="50px"/>',
            self.face_url,
        )
    image_data.short_description = u'人脸'