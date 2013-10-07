# coding: utf-8
import re
from django.db import models
from django.db.models.signals import post_save

from tagging.fields import TagField
from mptt.models import MPTTModel, TreeForeignKey
from lj.models import lj_crosspost
from victorkachalin.settings import production



class SinglePage(models.Model):
    name = models.CharField(max_length=255,unique=True)
    slug = models.CharField(max_length=50,unique=True)
    text = models.TextField()
    #category = models.ForeignKey(Category, null=True, limit_choices_to={'is_addable': True})
    class Meta:
        verbose_name = "страница"
        verbose_name_plural = "отдельные страницы" 
    def __unicode__(self):
        return self.name



# class BlogPost(models.Model):
    
#     name = models.CharField(max_length=255,unique=True)

#     date = models.DateField()
#     tags = TagField()
#     text = models.TextField()
#     category = 'blog'
    
#     def __unicode__(self):
#         return self.name
#     def get_absolute_url(self):
#         return '/blog/posts/{0}'.format(self.id)  
#     class Meta:
#         verbose_name = "запись в блоге"
#         verbose_name_plural = "записи в блоге"
#         ordering = ['-date']     


class Category(MPTTModel):
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children')
    name = models.CharField(max_length=50,unique=True)
    slug_keyword = models.CharField(max_length=50,unique=True, null=True)
    slug = models.CharField(max_length=50,unique=True, default='n/a')
    
    content_choices=(('/poems','стихи'),('/list','записи'),('cats','другие категории'),('/page','отдельная страница'))
    content = models.CharField(max_length=20,
                                choices=content_choices,
                                default='1') 
    is_addable = models.BooleanField(default=True)
    slug = models.CharField(max_length=50,unique=True)
    description = models.TextField()
    def __unicode__(self):

        name = ''  
        for item in self.get_ancestors(include_self=True):
            name+= ' - '+item.name
        return name[2:]    

        

    def get_absolute_url(self):

        return '/'+self.slug
    def save(self):
        #self.kw = self.slug
        if not self.slug_keyword + self.content in self.slug:
            if self.content == 'cats': # потому что нельзя сохранить пустое значение
                self.content = ''
            self.slug = self.slug_keyword + self.content 
        super(Category, self).save()  
    class Meta:
        verbose_name = "раздел"
        verbose_name_plural = "разделы"             
    
class NewPost(models.Model):

    name = models.CharField(max_length=255,unique=True)

    date = models.DateField()

    category = models.ForeignKey(Category, null=True, limit_choices_to={'is_addable': True})
    
    text = models.TextField()
    
    crosspost = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name
    def get_absolute_url(self):
        return '/{0}/{1}'.format(self.category.slug_keyword, self.id)
    class Meta:
        verbose_name = "запись"
        verbose_name_plural = "записи"
        ordering = ['-date']    
def get_default_blog():
    return Category.objects.get(slug_keyword='blog')
class BlogPost(NewPost):
    category = Category.objects.get(slug_keyword='blog')
    tags = TagField()
    class Meta:
        verbose_name = "запись в блоге"
        verbose_name_plural = "записи в блоге"
        ordering = ['-date'] 
    def save(self):
        self.category = Category.objects.get(slug_keyword='blog') 

if production.LJ_CROSSPOST_ENABLE:
    post_save.connect(lj_crosspost, sender=NewPost) 
    post_save.connect(lj_crosspost, sender=BlogPost) 