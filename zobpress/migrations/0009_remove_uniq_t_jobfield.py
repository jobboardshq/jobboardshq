
from south.db import db
from django.db import models
from zobpress.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Deleting unique_together for [job_form, order] on jobfieldmodel.
        db.delete_unique('zobpress_jobfieldmodel', ['job_form_id', 'order'])
        
    
    
    def backwards(self, orm):
        
        # Creating unique_together for [job_form, order] on jobfieldmodel.
        db.create_unique('zobpress_jobfieldmodel', ['job_form_id', 'order'])
        
    
    
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
        'zobpress.board': {
            'cost_per_job_listing': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'job_listing_expires': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'subdomain': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
        },
        'zobpress.boardextendedsettings': {
            'board': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['zobpress.Board']", 'unique': 'True', 'primary_key': 'True'}),
            'is_default_job_form': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'})
        },
        'zobpress.boardpayments': {
            'amount_for': ('django.db.models.fields.DateField', [], {}),
            'board': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['zobpress.Board']"}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': '1', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'job_payments': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'payment_type': ('django.db.models.fields.CharField', [], {'default': "'PayPal'", 'max_length': '10'}),
            'updated_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': '1', 'blank': 'True'})
        },
        'zobpress.boardpaypal': {
            'board': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['zobpress.Board']", 'unique': 'True', 'primary_key': 'True'}),
            'paypal_payer_id': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'paypal_token_gec': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'paypal_token_sec': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        'zobpress.boardsettings': {
            'analytics_code': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'board': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'settings'", 'unique': 'True', 'to': "orm['zobpress.Board']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'keywords': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'tag_line': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'template': ('django.db.models.fields.CharField', [], {'default': "'default'", 'max_length': '100'})
        },
        'zobpress.category': {
            'board': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['zobpress.Board']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '100', 'db_index': 'True'})
        },
        'zobpress.job': {
            'board': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['zobpress.Board']"}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['zobpress.Category']", 'null': 'True', 'blank': 'True'}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': '1', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_editable': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_expired': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'job_slug': ('django.db.models.fields.SlugField', [], {'max_length': '100', 'db_index': 'True'}),
            'job_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['zobpress.JobType']", 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'paypal_token_gec': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'paypal_token_sec': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'updated_on': ('django.db.models.fields.DateTimeField', [], {'auto_now': '1', 'blank': 'True'})
        },
        'zobpress.jobdata': {
            'data_type': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'job': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['zobpress.Job']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'value': ('django.db.models.fields.TextField', [], {})
        },
        'zobpress.jobfieldmodel': {
            'Meta': {'unique_together': "(('job_form', 'name'),)"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'job_form': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['zobpress.JobFormModel']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '10'}),
            'required': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'zobpress.jobfile': {
            'content_type': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'job': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['zobpress.Job']"}),
            'job_data': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['zobpress.JobData']"}),
            'public_path': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'uploaded_file': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'zobpress.jobformmodel': {
            'board': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['zobpress.Board']", 'unique': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'zobpress.jobtype': {
            'board': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['zobpress.Board']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('AutoSlugField', [], {'max_length': '100', 'populate_from': '"name"'})
        },
        'zobpress.page': {
            'content': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'job_board': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['zobpress.Board']"}),
            'page_slug': ('django.db.models.fields.SlugField', [], {'max_length': '100', 'db_index': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }
    
    complete_apps = ['zobpress']
