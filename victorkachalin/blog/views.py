# coding: utf-8
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView, TemplateView, FormView
from blog.models import NewPost, Category, BlogPost, SinglePage

from photologue.models import Gallery, Photo
from photologue.views import GalleryView
from tagging.models import Tag, TaggedItem



from django.http import HttpResponse
import datetime

def get_category_item(category): #helper function
    for item in Category.objects.all():
        if category in item.slug:
            return item

def write_context_all(context, **kwargs):
    kw_list = ['cname', 'cdescription', 'dododo', 'links', 'taglinks', 'object']
    for item in kw_list:
        if item in kwargs:
            context[item] = kwargs[item]


def write_context(self, context, item):

    is_child = item.is_child_node()
    dododo = item.get_root().name
    if is_child:
        links = item.get_root().get_descendants()[0].get_siblings(include_self=True)
    else:
        links = NewPost.objects.filter(category__slug=self.kwargs['cat'])
    write_context_all(context, dododo = dododo, links = links, cname = item.name, cdescription = item.description )    

class PhotoAlbumView(TemplateView):
    template_name = "photoalbum.html"

    def get_context_data(self, **kwargs):
    # Call the base implementation first to get a context

        context = super(PhotoAlbumView, self).get_context_data(**kwargs)
        
        gallery = Gallery.objects.get(title_slug='photoalbum')
        gallery_object = gallery.photos.all()
        tags = Tag.objects.usage_for_model(Photo)

        write_context_all(context, object = gallery_object, dododo='Категории', taglinks = tags, \
        cname='Фотоальбом', cdescription='Мои фотографии')

        return context


class PhotoAlbumTagView(PhotoAlbumView):
    def get_context_data(self, **kwargs):
    # Call the base implementation first to get a context

        context = super(PhotoAlbumView, self).get_context_data(**kwargs)

        tag = self.kwargs.get('tag', None)

        if tag:
            this_tag = Tag.objects.get(name=tag)
            gallery_object = TaggedItem.objects.get_union_by_model(Photo, this_tag)
        else:
            gallery_object = Gallery.objects.get(title_slug='photoalbum')
        tags = Tag.objects.usage_for_model(Photo)

        write_context_all(context, object = gallery_object, dododo='Категории', taglinks = tags, \
        cname='Фотоальбом', cdescription='Мои фотографии')

        return context

    def get_queryset(self):

        tag = self.kwargs.get('tag', None)
        if tag:
            this_tag = Tag.objects.get(name=tag)
            return TaggedItem.objects.get_union_by_model(Photo, this_tag)
        else:
            return BlogPost.objects.all()


class SinglePageView(TemplateView):
    template_name = "singlepage.html"
    kw = None

    def get_context_data(self, **kwargs):

        context = super(SinglePageView, self).get_context_data(**kwargs)
        context['object'] = SinglePage.objects.get(slug=self.kw)

        return context


class BlogPostListView(ListView):
    template_name = 'blogpost_list.html'
    model = BlogPost
    paginate_by = 3

    def get_context_data(self, **kwargs):

        context = super(BlogPostListView, self).get_context_data(**kwargs)
        item = get_category_item('blog')
        write_context_all(context, hasTags = True, dododo = 'Последние записи', links = BlogPost.objects.all(), \
        cname = item.name, cdescription = item.description )

        return context


class BlogPostTagListView(BlogPostListView):
    template_name = 'blogpost_detail.html'

    def get_queryset(self):
        #cat=self.kwargs['cat']
        tag = self.kwargs.get('tag', None)
        if tag:
            this_tag = Tag.objects.get(name=tag)
            return TaggedItem.objects.get_union_by_model(BlogPost, this_tag)
        else:
            return BlogPost.objects.all()


class BlogPostDetailView(DetailView):  # детализированное представление модели
    template_name = 'blogpost_detail.html'
    model = BlogPost

    def get_context_data(self, **kwargs):
    # Call the base implementation first to get a context
        context = super(BlogPostDetailView, self).get_context_data(**kwargs)
        item = get_category_item('blog')
        write_context_all(context, hasTags = True, dododo = 'Последние записи', links = BlogPost.objects.all(), \
        cname = item.name, cdescription = item.description )

        return context


def define_root_Cat(object):
    for item in Category.objects.all():
        if object.category == item.slug:
            return item.get_root()


class PostListView(ListView):
    model = NewPost
    paginate_by = 3

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        category = self.kwargs.get('cat', None)
        context = super(PostListView, self).get_context_data(**kwargs)
        item = get_category_item(category)
        write_context(self, context, item)

        return context

    def get_queryset(self):
        #cat=self.kwargs['cat']
        category = self.kwargs.get('cat', None)
        return NewPost.objects.filter(category__slug_keyword=category)




class CatListView(PostListView):
    paginate_by = 4

    def get_queryset(self):
        category = self.kwargs.get('cat', None)
        item = get_category_item(category)
        return item.get_descendants()

class PostDetailView(DetailView): # детализированное представление модели
    model = NewPost

    def get_context_data(self, **kwargs):
        
        context = super(PostDetailView, self).get_context_data(**kwargs)
        this_object = NewPost.objects.get(pk=self.kwargs['pk'])
        write_context(self, context, this_object.category)    

        return context


class HomePageView(GalleryView, DetailView):
    template_name = 'base_homepage.html'

    def get_object(self):
        gallery = get_object_or_404(Gallery, title_slug='homepage')
        return gallery.photos.all()
