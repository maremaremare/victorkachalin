# coding: utf-8
from blog.models import Category

def menu(request):
    return {"category" : Category,
    		'nodes': Category.objects.all()}