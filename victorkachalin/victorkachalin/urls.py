# coding: utf-8
from django.conf.urls import patterns, include, url
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from blog.views import PhotoAlbumTagView, PhotoAlbumView,\
    SinglePageView, SinglePageSidebarView, PostDetailView,\
    PostListView,  HomePageView, BlogPostListView,\
    BlogPostTagListView, BlogPostDetailView, CatListView
from shop.views import OrderFormView, OrderView, NewOrderView, UpdateOrderView


admin.autodiscover()

urlpatterns = patterns('',

    url(r'^$', HomePageView.as_view()),
    #url(r'^orders/$', NewOrderView.as_view(template_name='photo_buy.html')),
    url(r'^shop/orders/(?P<id>\w+)/edit$', UpdateOrderView.as_view(template_name='photo_buy.html')),
    url(r'^shop/orders/(?P<id>\w+)/(?P<action>\w+)$', NewOrderView.as_view(template_name='order.html')),
    url(r'^shop/orders/(?P<id>\w+)/$', NewOrderView.as_view(template_name='order.html')),
    url(r'^shop/orders/$', NewOrderView.as_view(template_name='order.html')),
    url(r'^home/$', HomePageView.as_view()),
    url(r'^blog/$', BlogPostListView.as_view()),
    url(r'^blog/page(?P<page>[0-9]+)/$', BlogPostListView.as_view()),
    url(r'^blog/(?P<pk>\d+)$', BlogPostDetailView.as_view()),
    url(r'^purchase/$', SinglePageView.as_view(template_name='singlepage.html', kw='purchase')),
    url(r'^thanks/$', SinglePageView.as_view(template_name='singlepage.html', kw='thanks')),
    url(r'^fail/$', SinglePageView.as_view(template_name='singlepage.html', kw='fail')),    
    url(r'^blog/tag/(?P<tag>\D+)/$', BlogPostTagListView.as_view(template_name='blogpost_list.html')),
    url(r'^blog/posts/(?P<pk>\d+)/$', BlogPostDetailView.as_view(template_name='blogpost_detail.html')),
    url(r'^photoalbum/$', PhotoAlbumView.as_view()),
    url(r'^photoalbum/tag/(?P<tag>\D+)/$', PhotoAlbumTagView.as_view()),
    url(r'^gallery/', include('photologue.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^(?P<slug>\w+)/page/$', SinglePageSidebarView.as_view()),
    url(r'^(?P<cat>\w+)/(?P<pk>\d+)$', PostDetailView.as_view()),
    #url(r'^\w+/(?P<pk>\d+)/$', PostDetailView.as_view()),
    url(r'^(?P<cat>\S+)/list/$',  PostListView.as_view(template_name='newpost_list.html')),
    url(r'^(?P<cat>\S+)/poems/$',  PostListView.as_view(template_name='poetry_list.html', paginate_by=12)),    
    url(r'^(?P<cat>\S+)/list/page(?P<page>[0-9]+)/$', PostListView.as_view(template_name='newpost_list.html')),
    url(r'^(?P<cat>\S+)/poems/page(?P<page>[0-9]+)/$', PostListView.as_view(template_name='poetry_list.html')),
    url(r'^(?P<cat>\w+)/$',  CatListView.as_view(template_name='cat_list.html', paginate_by=4)),
    url(r'^(?P<cat>\S+)/page(?P<page>[0-9]+)/$', PostListView.as_view(template_name='cat_list.html')),
    
    url(r'^gallery/photo/(?P<id>\S+)/buy/(?P<item>\w+)/$', OrderFormView.as_view(template_name='photo_buy.html'), name='buy'),
    url(r'^gallery/photo/(?P<id>\S+)/buy/(?P<item>\w+)/success/$', OrderView.as_view(template_name='photo_buy_success.html'), name='buy-success'),
    url(r'^grappelli/', include('grappelli.urls')),
)


