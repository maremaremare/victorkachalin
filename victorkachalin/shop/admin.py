# coding: utf-8
from django.contrib import admin

from shop.models import  Merchandise, Order

admin.site.register(Merchandise)
admin.site.register(Order) 