# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding index on 'MenuItem', fields ['is_enabled']
        db.create_index('menus_menuitem', ['is_enabled'])

        # Adding index on 'MenuItem', fields ['is_featured']
        db.create_index('menus_menuitem', ['is_featured'])

        # Adding index on 'MenuItem', fields ['publish_at']
        db.create_index('menus_menuitem', ['publish_at'])

        # Adding index on 'MenuItem', fields ['expire_at']
        db.create_index('menus_menuitem', ['expire_at'])

        # Adding index on 'Menu', fields ['is_enabled']
        db.create_index('menus_menu', ['is_enabled'])

        # Adding index on 'Menu', fields ['is_featured']
        db.create_index('menus_menu', ['is_featured'])

        # Adding index on 'Menu', fields ['publish_at']
        db.create_index('menus_menu', ['publish_at'])

        # Adding index on 'Menu', fields ['expire_at']
        db.create_index('menus_menu', ['expire_at'])

        # Adding index on 'WebLink', fields ['is_enabled']
        db.create_index('menus_weblink', ['is_enabled'])

        # Adding index on 'WebLink', fields ['is_featured']
        db.create_index('menus_weblink', ['is_featured'])

        # Adding index on 'WebLink', fields ['publish_at']
        db.create_index('menus_weblink', ['publish_at'])

        # Adding index on 'WebLink', fields ['expire_at']
        db.create_index('menus_weblink', ['expire_at'])

        # Adding index on 'ViewLink', fields ['is_enabled']
        db.create_index('menus_viewlink', ['is_enabled'])

        # Adding index on 'ViewLink', fields ['is_featured']
        db.create_index('menus_viewlink', ['is_featured'])

        # Adding index on 'ViewLink', fields ['publish_at']
        db.create_index('menus_viewlink', ['publish_at'])

        # Adding index on 'ViewLink', fields ['expire_at']
        db.create_index('menus_viewlink', ['expire_at'])


    def backwards(self, orm):
        # Removing index on 'ViewLink', fields ['expire_at']
        db.delete_index('menus_viewlink', ['expire_at'])

        # Removing index on 'ViewLink', fields ['publish_at']
        db.delete_index('menus_viewlink', ['publish_at'])

        # Removing index on 'ViewLink', fields ['is_featured']
        db.delete_index('menus_viewlink', ['is_featured'])

        # Removing index on 'ViewLink', fields ['is_enabled']
        db.delete_index('menus_viewlink', ['is_enabled'])

        # Removing index on 'WebLink', fields ['expire_at']
        db.delete_index('menus_weblink', ['expire_at'])

        # Removing index on 'WebLink', fields ['publish_at']
        db.delete_index('menus_weblink', ['publish_at'])

        # Removing index on 'WebLink', fields ['is_featured']
        db.delete_index('menus_weblink', ['is_featured'])

        # Removing index on 'WebLink', fields ['is_enabled']
        db.delete_index('menus_weblink', ['is_enabled'])

        # Removing index on 'Menu', fields ['expire_at']
        db.delete_index('menus_menu', ['expire_at'])

        # Removing index on 'Menu', fields ['publish_at']
        db.delete_index('menus_menu', ['publish_at'])

        # Removing index on 'Menu', fields ['is_featured']
        db.delete_index('menus_menu', ['is_featured'])

        # Removing index on 'Menu', fields ['is_enabled']
        db.delete_index('menus_menu', ['is_enabled'])

        # Removing index on 'MenuItem', fields ['expire_at']
        db.delete_index('menus_menuitem', ['expire_at'])

        # Removing index on 'MenuItem', fields ['publish_at']
        db.delete_index('menus_menuitem', ['publish_at'])

        # Removing index on 'MenuItem', fields ['is_featured']
        db.delete_index('menus_menuitem', ['is_featured'])

        # Removing index on 'MenuItem', fields ['is_enabled']
        db.delete_index('menus_menuitem', ['is_enabled'])


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'menus.menu': {
            'Meta': {'object_name': 'Menu'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'+'", 'to': "orm['auth.User']"}),
            'expire_at': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'db_index': 'True'}),
            'is_featured': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'publish_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'db_index': 'True'}),
            'publish_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'+'", 'null': 'True', 'to': "orm['auth.User']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'updated_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'+'", 'to': "orm['auth.User']"})
        },
        'menus.menuitem': {
            'Meta': {'ordering': "(u'order',)", 'object_name': 'MenuItem'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']", 'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'+'", 'to': "orm['auth.User']"}),
            'expire_at': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'is_enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'db_index': 'True'}),
            'is_featured': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'menu': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'items'", 'to': "orm['menus.Menu']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'object_id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'publish_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'db_index': 'True'}),
            'publish_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'+'", 'null': 'True', 'to': "orm['auth.User']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'updated_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'+'", 'to': "orm['auth.User']"})
        },
        'menus.viewlink': {
            'Meta': {'object_name': 'ViewLink'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'+'", 'to': "orm['auth.User']"}),
            'expire_at': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'db_index': 'True'}),
            'is_featured': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'publish_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'db_index': 'True'}),
            'publish_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'+'", 'null': 'True', 'to': "orm['auth.User']"}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'updated_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'+'", 'to': "orm['auth.User']"}),
            'view': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'menus.weblink': {
            'Meta': {'object_name': 'WebLink'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'+'", 'to': "orm['auth.User']"}),
            'expire_at': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'db_index': 'True'}),
            'is_featured': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'publish_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'db_index': 'True'}),
            'publish_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'+'", 'null': 'True', 'to': "orm['auth.User']"}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'updated_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'+'", 'to': "orm['auth.User']"}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['menus']