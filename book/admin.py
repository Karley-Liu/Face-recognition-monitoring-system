from django.contrib import admin

from book import models
from django.shortcuts import render
# class AdminSite(admin.AdminSite):
#     site_title = 'Karlin的管理系统'
#     site_header = 'Karlin的管理系统'

# site = MyAdminSite()
from book.views import bookviews


@admin.register(models.Book)
class BookAdmin(admin.ModelAdmin):
    # list_display = ('id','name','price','pub_date')
    # list_per_page = 3
    def changelist_view(self, request, extra_content=None):
        return bookviews(request)


# admin.site.register(models.Book,BookAdmin)