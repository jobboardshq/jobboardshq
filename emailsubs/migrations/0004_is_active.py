
from south.db import db
from django.db import models
from emailsubs.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Deleting unique_together for [email] on emailsubscription.
        db.delete_unique('emailsubs_emailsubscription', ['email'])
        
        # Adding field 'EmailSubscription.is_active'
        db.add_column('emailsubs_emailsubscription', 'is_active', orm['emailsubs.emailsubscription:is_active'])
        
        # Adding field 'EmailSubscription.created_on'
        db.add_column('emailsubs_emailsubscription', 'created_on', orm['emailsubs.emailsubscription:created_on'])
        
        # Deleting field 'EmailSubscription.created'
        db.delete_column('emailsubs_emailsubscription', 'created')
        
        # Creating unique_together for [board, email] on EmailSubscription.
        db.create_unique('emailsubs_emailsubscription', ['board_id', 'email'])
        
    
    
    def backwards(self, orm):
        
        # Deleting unique_together for [board, email] on EmailSubscription.
        db.delete_unique('emailsubs_emailsubscription', ['board_id', 'email'])
        
        # Deleting field 'EmailSubscription.is_active'
        db.delete_column('emailsubs_emailsubscription', 'is_active')
        
        # Deleting field 'EmailSubscription.created_on'
        db.delete_column('emailsubs_emailsubscription', 'created_on')
        
        # Adding field 'EmailSubscription.created'
        db.add_column('emailsubs_emailsubscription', 'created', orm['emailsubs.emailsubscription:created'])
        
        # Creating unique_together for [email] on emailsubscription.
        db.create_unique('emailsubs_emailsubscription', ['email'])
        
    
    
    models = {
        'auth.group': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'unique_together': "(('content_type', 'codename'),)"},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'unique_together': "(('app_label', 'model'),)", 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'emailsubs.emailsent': {
            'board': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['zobpress.Board']", 'unique': 'True'}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': '1', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'num_times_sent': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'updated_on': ('django.db.models.fields.DateTimeField', [], {'auto_now': '1', 'blank': 'True'})
        },
        'emailsubs.emailsubscription': {
            'Meta': {'unique_together': "(('board', 'email'),)"},
            'board': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['zobpress.Board']"}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'is_confirmed': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'zobpress.board': {
            'cost_per_job_listing': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'job_listing_expires': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'subdomain': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
        }
    }
    
    complete_apps = ['emailsubs']
