from django.contrib import admin

# Register your models here.
from django.utils.safestring import mark_safe

from faces import models


@admin.register(models.Faces)
class FacesAdmin(admin.ModelAdmin):
    list_display = ('id','image_data','face_date')
    readonly_fields = ('face_url',)
    list_per_page = 15
    # def image_data(self,obj):
    #     return mark_safe(u'<img src="%s" width="100px" />' % obj.image_data)
