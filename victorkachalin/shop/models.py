# coding: utf-8
import uuid
from django.db import models
from photologue.models import Photo

# Create your models here.
class Item(models.Model):
    name = models.CharField(max_length=255,unique=True)
    slug = models.CharField(max_length=50,unique=True)
    link_text = models.CharField(max_length=255,unique=True, help_text=u'Текст ссылки на товар')
    price = models.IntegerField()
    options =  models.CharField(max_length=255,unique=False, blank = True, help_text=u'Доступные покупателю варианты товара на выбор (генерируется drop-down список). Варианты разделяются запятой с пробелом. Несколько списков разделяются символом #') 
    is_original_needed = models.BooleanField(default = False, help_text=u'Нужно ли иметь оригинал рисунка, чтобы это продавать')  
    def __unicode__(self):
        return self.name


    class Meta:
        verbose_name = "товар"
        verbose_name_plural = "товары" 

    # def save(self, *args, **kwargs):
    #     if self.options:
    #         result = []
    #         str = self.options
    #         biglist = str.split('#')
    #         for i in range(len(biglist)):
    #             result.append(biglist[i].split(', '))
    #         self.options = result    

    #     super(Item, self).save(*args, **kwargs)        

def get_img_src(slug):
    photo = Photo.objects.get(title_slug=slug)
    return photo.get_admin_thumbnail_url()



class Order(models.Model):
    name = models.CharField(('Имя заказчика'), max_length=255,unique=False)
    email = models.EmailField()
    address = models.CharField(('Адрес'), max_length=255,unique=False, blank=True, help_text=u'Адрес доставки, если выбрана доставка почтой')
    phone = models.CharField(('Телефон'), max_length=255,unique=False)
    merchandise_id = models.CharField(('Что заказано'), max_length=255,unique=False)
    photo_id = models.CharField(('Название рисунка'), max_length=255, unique=False, blank=True)
    extra_field = models.CharField(('Детали'), max_length=255,unique=False)
    created_at = models.DateTimeField(auto_now_add = True)
    order_id = models.IntegerField(('Номер'),unique=True, blank=True, help_text=u'Уникальный номер заказа')
    postal = models.BooleanField(('Доставка почтой'),default = False)
    meeting = models.BooleanField(('Личная встреча'),default = False)

    def admin_thumbnail(self):
   
        return '<a href="%s"><img src="%s"></a>' % ('http://victorkachalin.ru/gallery/'+self.photo_id, 'http://victorkachalin.ru/'+get_img_src(self.photo_id))
    admin_thumbnail.allow_tags = True

    def __unicode__(self):
        return str(self.order_id) #self.name+ "   %s" % str(self.created_at)[:16]
    class Meta:
        verbose_name = "заказ"
        verbose_name_plural = "заказы" 
    def save(self, *args, **kwargs):
        if self.address:
            self.postal = True
            self.meeting = False
        else:
            self.postal = False
            self.meeting = True    
  

        super(Order, self).save(*args, **kwargs)  