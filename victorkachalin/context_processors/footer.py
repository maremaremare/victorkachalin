# coding: utf-8
from blog.models import NewPost, BlogPost
from photologue.models import Photo, Gallery

def footer(request):
    return {
    		'poetry': NewPost.objects.filter(category='latest_poems'),
    		'blogposts': BlogPost.objects.all(),
    		'pictures': Photo.objects.filter(is_public='True'),
    		'galleries': Gallery.objects.filter(is_public='True')



    		}