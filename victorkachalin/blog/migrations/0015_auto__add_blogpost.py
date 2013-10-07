# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'BlogPost'
        db.create_table(u'blog_blogpost', (
            (u'newpost_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['blog.NewPost'], unique=True, primary_key=True)),
            ('tags', self.gf('tagging.fields.TagField')()),
        ))
        db.send_create_signal(u'blog', ['BlogPost'])


    def backwards(self, orm):
        # Deleting model 'BlogPost'
        db.delete_table(u'blog_blogpost')


    models = {
        u'blog.blogpost': {
            'Meta': {'ordering': "['-date']", 'object_name': 'BlogPost', '_ormbases': [u'blog.NewPost']},
            u'newpost_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['blog.NewPost']", 'unique': 'True', 'primary_key': 'True'}),
            'tags': ('tagging.fields.TagField', [], {})
        },
        u'blog.category': {
            'Meta': {'object_name': 'Category'},
            'content': ('django.db.models.fields.CharField', [], {'default': "'1'", 'max_length': '20'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_addable': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            u'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': u"orm['blog.Category']"}),
            u'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'slug': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'slug_keyword': ('django.db.models.fields.CharField', [], {'max_length': '50', 'unique': 'True', 'null': 'True'}),
            u'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        u'blog.newpost': {
            'Meta': {'ordering': "['-date']", 'object_name': 'NewPost'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['blog.Category']", 'null': 'True'}),
            'crosspost': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'date': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'text': ('django.db.models.fields.TextField', [], {})
        },
        u'blog.singlepage': {
            'Meta': {'object_name': 'SinglePage'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'slug': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'text': ('django.db.models.fields.TextField', [], {})
        }
    }

    complete_apps = ['blog']