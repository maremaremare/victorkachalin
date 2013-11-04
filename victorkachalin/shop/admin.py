# coding: utf-8
from django.contrib import admin

from shop.models import  Item, Order

class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'merchandise_id', 'phone', 'email', 'postal', 'meeting', 'admin_thumbnail')
    exclude = ('order_id',)

admin.site.register(Item)
admin.site.register(Order, OrderAdmin) 