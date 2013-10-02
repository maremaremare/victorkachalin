# coding: utf-8
from django.contrib import admin
from django.contrib.auth.models import User, Group
from treeadmin.admin import TreeAdmin
from blog.models import NewPost, BlogPost, Category, SinglePage # наша модель из blog/models.py


class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'date')
    list_filter = ('category','date')
    change_list_filter_template = "admin/filter_listing.html"
    class Media:
        js = ['/static/grappelli/tinymce/jscripts/tiny_mce/tiny_mce.js',
			  '/static/grappelli/tinymce_setup/tinymce_setup.js' ]


class TreeModelAdmin(TreeAdmin):
	# class Media:
 #        js = ['/static/grappelli/tinymce/jscripts/tiny_mce/tiny_mce.js',
 #              '/static/grappelli/tinymce_setup/tinymce_setup.js' ]
    pass


admin.site.unregister(User)
admin.site.unregister(Group)           
admin.site.register(BlogPost)
admin.site.register(SinglePage)        
admin.site.register(Category, TreeModelAdmin)
admin.site.register(NewPost, UserAdmin) 

