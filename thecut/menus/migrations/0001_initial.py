# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models
from thecut.authorship.settings import AUTH_USER_MODEL

class Migration(SchemaMigration):

    def forwards(self, orm):

        # Adding model 'Menu'
        db.create_table('menus_menu', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('is_enabled', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('is_featured', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('publish_at', self.gf('django.db.models.fields.DateTimeField')()),
            ('publish_by', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='menu_publish_by_user', null=True, to=orm[AUTH_USER_MODEL])),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(related_name='menu_created_by_user', to=orm[AUTH_USER_MODEL])),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('updated_by', self.gf('django.db.models.fields.related.ForeignKey')(related_name='menu_updated_by_user', to=orm[AUTH_USER_MODEL])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=50, db_index=True)),
        ))
        db.send_create_signal('menus', ['Menu'])

        # Adding model 'MenuItem'
        db.create_table('menus_menuitem', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('is_enabled', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('is_featured', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('publish_at', self.gf('django.db.models.fields.DateTimeField')()),
            ('publish_by', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='menuitem_publish_by_user', null=True, to=orm[AUTH_USER_MODEL])),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(related_name='menuitem_created_by_user', to=orm[AUTH_USER_MODEL])),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('updated_by', self.gf('django.db.models.fields.related.ForeignKey')(related_name='menuitem_updated_by_user', to=orm[AUTH_USER_MODEL])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('order', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('menu', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['menus.Menu'])),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
            ('object_id', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('menus', ['MenuItem'])

        # Adding model 'ViewLink'
        db.create_table('menus_viewlink', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('is_enabled', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('is_featured', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('publish_at', self.gf('django.db.models.fields.DateTimeField')()),
            ('publish_by', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='viewlink_publish_by_user', null=True, to=orm[AUTH_USER_MODEL])),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(related_name='viewlink_created_by_user', to=orm[AUTH_USER_MODEL])),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('updated_by', self.gf('django.db.models.fields.related.ForeignKey')(related_name='viewlink_updated_by_user', to=orm[AUTH_USER_MODEL])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('view', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('menus', ['ViewLink'])

        # Adding model 'WebLink'
        db.create_table('menus_weblink', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('is_enabled', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('is_featured', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('publish_at', self.gf('django.db.models.fields.DateTimeField')()),
            ('publish_by', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='weblink_publish_by_user', null=True, to=orm[AUTH_USER_MODEL])),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(related_name='weblink_created_by_user', to=orm[AUTH_USER_MODEL])),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('updated_by', self.gf('django.db.models.fields.related.ForeignKey')(related_name='weblink_updated_by_user', to=orm[AUTH_USER_MODEL])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
        ))
        db.send_create_signal('menus', ['WebLink'])


    def backwards(self, orm):

        # Deleting model 'Menu'
        db.delete_table('menus_menu')

        # Deleting model 'MenuItem'
        db.delete_table('menus_menuitem')

        # Deleting model 'ViewLink'
        db.delete_table('menus_viewlink')

        # Deleting model 'WebLink'
        db.delete_table('menus_weblink')


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
        AUTH_USER_MODEL: {
            'Meta': {'object_name': AUTH_USER_MODEL.split('.')[-1]},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'menus.menu': {
            'Meta': {'ordering': "['-created_at']", 'object_name': 'Menu'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'menu_created_by_user'", 'to': "orm['{0}']".format(AUTH_USER_MODEL)}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_featured': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'publish_at': ('django.db.models.fields.DateTimeField', [], {}),
            'publish_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'menu_publish_by_user'", 'null': 'True', 'to': "orm['{0}']".format(AUTH_USER_MODEL)}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50', 'db_index': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'updated_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'menu_updated_by_user'", 'to': "orm['{0}']".format(AUTH_USER_MODEL)})
        },
        'menus.menuitem': {
            'Meta': {'ordering': "['order']", 'object_name': 'MenuItem'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'menuitem_created_by_user'", 'to': "orm['{0}']".format(AUTH_USER_MODEL)}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_featured': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'menu': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['menus.Menu']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'object_id': ('django.db.models.fields.IntegerField', [], {}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'publish_at': ('django.db.models.fields.DateTimeField', [], {}),
            'publish_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'menuitem_publish_by_user'", 'null': 'True', 'to': "orm['{0}']".format(AUTH_USER_MODEL)}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'updated_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'menuitem_updated_by_user'", 'to': "orm['{0}']".format(AUTH_USER_MODEL)})
        },
        'menus.viewlink': {
            'Meta': {'ordering': "['-created_at']", 'object_name': 'ViewLink'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'viewlink_created_by_user'", 'to': "orm['{0}']".format(AUTH_USER_MODEL)}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_featured': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'publish_at': ('django.db.models.fields.DateTimeField', [], {}),
            'publish_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'viewlink_publish_by_user'", 'null': 'True', 'to': "orm['{0}']".format(AUTH_USER_MODEL)}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'updated_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'viewlink_updated_by_user'", 'to': "orm['{0}']".format(AUTH_USER_MODEL)}),
            'view': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'menus.weblink': {
            'Meta': {'ordering': "['-created_at']", 'object_name': 'WebLink'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'weblink_created_by_user'", 'to': "orm['{0}']".format(AUTH_USER_MODEL)}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_featured': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'publish_at': ('django.db.models.fields.DateTimeField', [], {}),
            'publish_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'weblink_publish_by_user'", 'null': 'True', 'to': "orm['{0}']".format(AUTH_USER_MODEL)}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'updated_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'weblink_updated_by_user'", 'to': "orm['{0}']".format(AUTH_USER_MODEL)}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['menus']
