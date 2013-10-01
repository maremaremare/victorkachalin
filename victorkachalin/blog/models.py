# coding: utf-8
from django.db import models
from tagging.fields import TagField
# Create your models here.

from mptt.models import MPTTModel, TreeForeignKey

import re



class SinglePage(models.Model):
    name = models.CharField(max_length=255,unique=True)
    slug = models.CharField(max_length=50,unique=True)
    text = models.TextField()
    class Meta:
        verbose_name = "страница"
        verbose_name_plural = "отдельные страницы" 



class BlogPost(models.Model):
    
    name = models.CharField(max_length=255,unique=True)

    date = models.DateField()
    tags = TagField()
    text = models.TextField()
    
    def __unicode__(self):
        return self.name
    def get_absolute_url(self):
        return '/blog/posts/{0}'.format(self.id)  
    class Meta:
        verbose_name = "запись в блоге"
        verbose_name_plural = "записи в блоге"
        ordering = ['-date']     


class Cat(MPTTModel):
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')
    name = models.CharField(max_length=50,unique=True)
    slug = models.CharField(max_length=50,unique=True)
    content_choices=(('/poetry','стихи'),('/list','записи'),('','другие категории'),('/page','отдельная страница'))
    content = models.CharField(max_length=20,
                                choices=content_choices,
                                default='1') 
    is_addable = models.BooleanField(default=True)
    slug = models.CharField(max_length=50,unique=True)
    description = models.TextField()
    def __unicode__(self):
        return self.name
    def get_absolute_url(self):
        return '/'+self.slug
    def save(self):
        if not self.content in self.slug:
            self.slug += self.content 
        super(Cat, self).save()  
    class Meta:
        verbose_name = "раздел"
        verbose_name_plural = "разделы"             
    
class NewPost(models.Model):

    def create_choices(): #TODO убрать лишнее
        list=[]
        
        for item in Cat.objects.all():
            if not item.get_children() and item.is_addable:
                category = item.slug.split('/')[0]
                if item.get_root().name != item.name:
                    list.append((category,item.get_root().name+':     '+item.name))
                else:
                    list.append((category, item.name))
        return list    
    #tags = TaggableManager()
    #category_choices=(('blog','blog'),('poetry','poetry'),('3','friends_poetry'),('4','selected'),('5','standalone'))
    category_choices=create_choices()
    name = models.CharField(max_length=255,unique=True)

    date = models.DateField()
    category = models.CharField(max_length=20,
                                choices=category_choices,
                                default='1')
    def define_root_category(self):
        for item in Category.objects.all():
            if self.category == item.slug:
                return item.get_root().name
    #root_category = define_root_category(self)            
    text = models.TextField()
    
    def __unicode__(self):
        return self.name
    def get_absolute_url(self):
        return '/{0}/{1}'.format(self.category, self.id)
    class Meta:
        verbose_name = "запись"
        verbose_name_plural = "записи"
        ordering = ['-date']    