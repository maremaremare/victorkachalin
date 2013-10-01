# coding: utf-8
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView, TemplateView, FormView
from blog.models import NewPost, Cat, BlogPost, SinglePage

from photologue.models import Gallery, Photo
from photologue.views import GalleryView
from tagging.models import Tag, TaggedItem


class PhotoAlbumView(TemplateView):
    template_name = "photoalbum.html"

    def get_context_data(self, **kwargs):
    # Call the base implementation first to get a context

        context = super(PhotoAlbumView, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        #context['sidebar_title'] = define_root_Cat(request)
        c = None
        for item in Cat.objects.all():
            if 'about' == item.slug:
                c = item
        gallery = Gallery.objects.get(title_slug='photoalbum')
        context['object'] = gallery.photos.all()
        tags = Tag.objects.usage_for_model(Photo)
        context['hastags'] = False
        context['dododo'] = 'Категории'
        context['taglinks'] = tags
        context['cname'] = 'Фотоальбом'
        context['cdescription'] = 'Мои фотографии'
        return context


class PhotoAlbumTagView(PhotoAlbumView):
    def get_context_data(self, **kwargs):
    # Call the base implementation first to get a context

        context = super(PhotoAlbumView, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        #context['sidebar_title'] = define_root_Cat(request)
        tag = self.kwargs.get('tag', None)
        if tag:
            this_tag = Tag.objects.get(name=tag)
        c = None
        for item in Cat.objects.all():
            if 'about' == item.slug:
                c = item
        if tag:
            this_tag = Tag.objects.get(name=tag)
            context['object'] = TaggedItem.objects.get_union_by_model(Photo, this_tag)
        else:
            context['object'] = Gallery.objects.get(title_slug='photoalbum')
        tags = Tag.objects.usage_for_model(Photo)
        context['hastags'] = False
        context['dododo'] = 'Категории'
        context['taglinks'] = tags
        context['cname'] = 'Фотоальбом'
        context['cdescription'] = 'Мои фотографии'
        return context

    def get_queryset(self):
        #cat=self.kwargs['cat']
        tag = self.kwargs.get('tag', None)
        if tag:
            this_tag = Tag.objects.get(name=tag)
            #string =  TaggedItem.objects.get_union_by_model(BlogPost, this_tag)
            return TaggedItem.objects.get_union_by_model(Photo, this_tag)
        else:
            return BlogPost.objects.all()


class SinglePageView(TemplateView):
    template_name = "singlepage.html"
    kw = None

    def get_context_data(self, **kwargs):
    # Call the base implementation first to get a context

        context = super(SinglePageView, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        #context['sidebar_title'] = define_root_Cat(request) 
        context['object'] = SinglePage.objects.get(slug=self.kw)

        return context


class BlogPostListView(ListView):
    template_name = 'blogpost_list.html'
    model = BlogPost
    paginate_by = 3

    def get_context_data(self, **kwargs):
    # Call the base implementation first to get a context

        context = super(BlogPostListView, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        #context['sidebar_title'] = define_root_Cat(request) 
        c = None
        for item in Cat.objects.all():
            if 'blog' == item.slug:
                c = item

        context['hastags'] = True
        context['dododo'] = 'Последние записи'
        context['links'] = BlogPost.objects.all()
        context['cname'] = c.name
        context['cdescription'] = c.description
        return context


class BlogPostTagListView(BlogPostListView):
    template_name = 'blogpost_detail.html'

    def get_queryset(self):
        #cat=self.kwargs['cat']
        tag = self.kwargs.get('tag', None)
        if tag:
            this_tag = Tag.objects.get(name=tag)
            #string =  TaggedItem.objects.get_union_by_model(BlogPost, this_tag)
            return TaggedItem.objects.get_union_by_model(BlogPost, this_tag)
        else:
            return BlogPost.objects.all()


class BlogPostDetailView(DetailView):  # детализированное представление модели
    template_name = 'blogpost_detail.html'
    model = BlogPost

    def get_context_data(self, **kwargs):
    # Call the base implementation first to get a context
        context = super(BlogPostDetailView, self).get_context_data(**kwargs)
        name = None
        for item in Cat.objects.all():
            if 'blog' in item.slug:
                context['cname'] = item.name
                context['cdescription'] = item.description

        context['hastags'] = True
        context['dododo'] = 'Последние записи'
        context['links'] = BlogPost.objects.all()
        context['category'] = name

        return context


def define_root_Cat(object):
    for item in Cat.objects.all():
        if object.category == item.slug:
            return item.get_root()


class PostListView(ListView):
    model = NewPost
    paginate_by = 3

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        cat = self.kwargs.get('cat', None)

        context = super(PostListView, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        #context['sidebar_title'] = define_root_Cat(request) 

        for item in Cat.objects.all():
            if cat in item.slug:
                is_child = item.is_child_node()
                name = item.get_root().name
                desc = item.get_root().get_descendants()
                context['cslug'] = cat
                context['cname'] = item.name
                context['cdescription'] = item.description
                if is_child:
                    context['dododo'] = name
                    context['links'] = desc
                    print desc
                else:
                    context['dododo'] = 'Последние записи'
                    context['links'] = NewPost.objects.filter(category=self.kwargs['cat'])

        return context

    def get_queryset(self):
        #cat=self.kwargs['cat']
        catt = self.kwargs.get('cat', None)
        return NewPost.objects.filter(category=catt)


class CatListView(PostListView):
    paginate_by = 4

    def get_queryset(self):
        catt = self.kwargs.get('cat', None)
        for item in Cat.objects.all():
            if catt in item.slug:
                return item.get_descendants()


class PostDetailView(DetailView): # детализированное представление модели
    model = NewPost

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(PostDetailView, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        #context['sidebar_title'] = define_root_Cat(request)
        this_object = NewPost.objects.get(pk=self.kwargs['pk'])

        for item in Cat.objects.all():
            if this_object.category in item.slug:
                is_child = item.is_child_node()
                root = item.get_root()
        context['cname'] = root.name
        context['cdescription'] = root.description
        context['dododo'] = root.name
        context['links'] = root.get_descendants()

        return context


class HomePageView(GalleryView, DetailView):
    template_name = 'base_homepage.html'

    def get_object(self):
        gallery = get_object_or_404(Gallery, title_slug='homepage')
        return gallery.photos.all()
