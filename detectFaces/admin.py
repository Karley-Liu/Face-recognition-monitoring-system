from django.contrib import admin

# Register your models here.
from record import models


@admin.register(models.Record)
class detectFacesAdmin(admin.ModelAdmin):
    # def changelist_view(self, request, extra_content=None):
    #     return detectFaces(request)
    # list_display = ('id','datetime')
    # list_display_links =
    pass