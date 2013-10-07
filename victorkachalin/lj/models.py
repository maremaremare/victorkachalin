# coding=UTF-8
from django.db import models
from django.conf import settings


import xmlrpclib
from datetime import datetime
from md5 import md5






class LiveJournalPost(models.Model):
    post_id = models.IntegerField(editable=False)
    lj_id = models.IntegerField(editable=False)

def create_args(blog_tags, local_post, remote_post=None):
    now = datetime.now()
    auth_challenge, auth_response = lj_challenge()
    #current_site = Site.objects.get(id=settings.SITE_ID)
    event = local_post.text#u'%s<lj-cut>%s<br/>Оригинал можно почитать на <a href="http://%s/blog/%s/%s/">http://akademic.name</a></lj-cut>'%(local_post.excerpt.rendered, local_post.content.rendered, local_post.date_published.year, local_post.slug )
  
    # else:
    #     tags = ''
    if blog_tags:
        tags = local_post.tags
    else:    
        cats = local_post.category.__unicode__()
        tag_list = cats.split(' - ')

        tags = ','.join(tag_list)
 
    # tags = '' 
    args = {
            'auth_method' : 'challenge',
            'auth_challenge' : auth_challenge,
            'auth_response' : auth_response,
            'security' : 'public',
            'lineendings' : 'unix',
            'ver' : '1',
            'username' : settings.LJ_USERNAME, 
            'clientversion' : 'Akademic-Connector/0.0.2',
            'event' : event,
            'subject' : local_post.name,
            'year' : now.year,
            'mon' : now.month,
            'day' : now.day,
            'hour': now.hour,
            'min' : now.minute,
            'props' : {
                'taglist' : tags,
                'opt_backdated' : True,
                'opt_preformatted' : True,
            }
    }

    if remote_post:
        args['itemid'] = remote_post

    return args

def lj_challenge():
    server = xmlrpclib.ServerProxy('http://www.livejournal.com/interface/xmlrpc')
    response = server.LJ.XMLRPC.getchallenge()
    auth_challenge = response['challenge']

    try:
        password_md5 = settings.LJ_PASSWORD_MD5
    except AttributeError:
        password_md5 = md5( settings.LJ_PASS ).hexdigest()

    auth_response = md5( auth_challenge + password_md5 ).hexdigest()
    return ( auth_challenge, auth_response )

def lj_edit(local_post, remote_post, blog_tags):
    server = xmlrpclib.ServerProxy('http://www.livejournal.com/interface/xmlrpc')
    response = server.LJ.XMLRPC.editevent(create_args(blog_tags, local_post, remote_post))

def lj_create(local_post, blog_tags):
    server = xmlrpclib.ServerProxy('http://www.livejournal.com/interface/xmlrpc')
    response = server.LJ.XMLRPC.postevent(create_args(blog_tags, local_post))

    LiveJournalPost.objects.create(post_id=local_post.id, lj_id=response.get('itemid')).save()

def lj_crosspost(sender, **kwargs):
    instance = kwargs['instance']
    max_non_edit = datetime.strptime( '2010-01-07 22:22:37', '%Y-%m-%d %H:%M:%S' ) #post with id 77
    #if instance.is_published and instance.date_published > max_non_edit :
    post_id = instance.pk
    blog_tags = False
    if hasattr(sender, 'tags'):
        blog_tags = True
    if instance.crosspost:
        try:
            post = LiveJournalPost.objects.get(post_id=post_id)
            lj_edit(instance, post.lj_id, blog_tags)
        except LiveJournalPost.DoesNotExist:
            lj_create(instance, blog_tags)