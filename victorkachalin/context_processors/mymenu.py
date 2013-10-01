# coding: utf-8
from blog.models import Cat

def menu(request):
    return {"category" : Cat,
    		'nodes': Cat.objects.all()}