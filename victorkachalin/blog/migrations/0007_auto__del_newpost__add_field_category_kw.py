# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'NewPost'
        db.delete_table(u'blog_newpost')

        # Adding field 'Category.kw'
        db.add_column(u'blog_category', 'kw',
                      self.gf('django.db.models.fields.CharField')(max_length=50, unique=True, null=True),
                      keep_default=False)


    def backwards(self, orm):
        # Adding model 'NewPost'
        db.create_table(u'blog_newpost', (
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['blog.Category'], null=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255, unique=True)),
            ('text', self.gf('django.db.models.fields.TextField')()),
            ('date', self.gf('django.db.models.fields.DateField')()),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'blog', ['NewPost'])

        # Deleting field 'Category.kw'
        db.delete_column(u'blog_category', 'kw')


    models = {
        u'blog.blogpost': {
            'Meta': {'ordering': "['-date']", 'object_name': 'BlogPost'},
            'date': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'tags': ('tagging.fields.TagField', [], {}),
            'text': ('django.db.models.fields.TextField', [], {})
        },
        u'blog.category': {
            'Meta': {'object_name': 'Category'},
            'content': ('django.db.models.fields.CharField', [], {'default': "'1'", 'max_length': '20'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_addable': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'kw': ('django.db.models.fields.CharField', [], {'max_length': '50', 'unique': 'True', 'null': 'True'}),
            u'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            u'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': u"orm['blog.Category']"}),
            u'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'slug': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            u'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
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