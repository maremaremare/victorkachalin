# coding: utf-8
from django.db import models

# Create your models here.
class Merchandise(models.Model):
    name = models.CharField(max_length=255,unique=True)
    slug = models.CharField(max_length=50,unique=True)
    price = models.IntegerField()
    options =  models.CharField(max_length=255,unique=False, blank = True)   
    def __unicode__(self):
        return self.name
    class Meta:
        verbose_name = "товар"
        verbose_name_plural = "товары"     

class Order(models.Model):
    name = models.CharField(max_length=255,unique=False)
    email = models.EmailField()
    address = models.CharField(max_length=255,unique=False)
    phone = models.CharField(max_length=255,unique=False)
    merchandise_id = models.CharField(max_length=255,unique=False)
    extra_field = models.CharField(max_length=255,unique=False)
    created_at = models.DateTimeField(auto_now_add = True)
    def __unicode__(self):
        return self.name+ "   %s" % str(self.created_at)[:16]
    class Meta:
        verbose_name = "заказ"
        verbose_name_plural = "заказы"     