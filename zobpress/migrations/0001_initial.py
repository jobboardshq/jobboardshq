
from south.db import db
from django.db import models
from zobpress.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'Board'
        db.create_table('zobpress_board', (
            ('id', orm['zobpress.Board:id']),
            ('subdomain', orm['zobpress.Board:subdomain']),
            ('domain', orm['zobpress.Board:domain']),
            ('name', orm['zobpress.Board:name']),
            ('description', orm['zobpress.Board:description']),
            ('job_listing_expires', orm['zobpress.Board:job_listing_expires']),
            ('cost_per_job_listing', orm['zobpress.Board:cost_per_job_listing']),
            ('owner', orm['zobpress.Board:owner']),
        ))
        db.send_create_signal('zobpress', ['Board'])
        
        # Adding model 'JobFile'
        db.create_table('zobpress_jobfile', (
            ('id', orm['zobpress.JobFile:id']),
            ('job', orm['zobpress.JobFile:job']),
            ('job_data', orm['zobpress.JobFile:job_data']),
            ('uploaded_file', orm['zobpress.JobFile:uploaded_file']),
            ('public_path', orm['zobpress.JobFile:public_path']),
            ('content_type', orm['zobpress.JobFile:content_type']),
        ))
        db.send_create_signal('zobpress', ['JobFile'])
        
        # Adding model 'JobFieldModel'
        db.create_table('zobpress_jobfieldmodel', (
            ('id', orm['zobpress.JobFieldModel:id']),
            ('job_form', orm['zobpress.JobFieldModel:job_form']),
            ('name', orm['zobpress.JobFieldModel:name']),
            ('type', orm['zobpress.JobFieldModel:type']),
            ('order', orm['zobpress.JobFieldModel:order']),
        ))
        db.send_create_signal('zobpress', ['JobFieldModel'])
        
        # Adding model 'JobData'
        db.create_table('zobpress_jobdata', (
            ('id', orm['zobpress.JobData:id']),
            ('job', orm['zobpress.JobData:job']),
            ('data_type', orm['zobpress.JobData:data_type']),
            ('name', orm['zobpress.JobData:name']),
            ('value', orm['zobpress.JobData:value']),
        ))
        db.send_create_signal('zobpress', ['JobData'])
        
        # Adding model 'JobFormModel'
        db.create_table('zobpress_jobformmodel', (
            ('id', orm['zobpress.JobFormModel:id']),
            ('board', orm['zobpress.JobFormModel:board']),
        ))
        db.send_create_signal('zobpress', ['JobFormModel'])
        
        # Adding model 'BoardExtendedSettings'
        db.create_table('zobpress_boardextendedsettings', (
            ('board', orm['zobpress.BoardExtendedSettings:board']),
            ('is_default_job_form', orm['zobpress.BoardExtendedSettings:is_default_job_form']),
        ))
        db.send_create_signal('zobpress', ['BoardExtendedSettings'])
        
        # Adding model 'BoardPayments'
        db.create_table('zobpress_boardpayments', (
            ('id', orm['zobpress.BoardPayments:id']),
            ('board', orm['zobpress.BoardPayments:board']),
            ('amount_for', orm['zobpress.BoardPayments:amount_for']),
            ('job_payments', orm['zobpress.BoardPayments:job_payments']),
            ('payment_type', orm['zobpress.BoardPayments:payment_type']),
            ('created_on', orm['zobpress.BoardPayments:created_on']),
            ('updated_on', orm['zobpress.BoardPayments:updated_on']),
        ))
        db.send_create_signal('zobpress', ['BoardPayments'])
        
        # Adding model 'BoardPayPal'
        db.create_table('zobpress_boardpaypal', (
            ('board', orm['zobpress.BoardPayPal:board']),
            ('paypal_token_sec', orm['zobpress.BoardPayPal:paypal_token_sec']),
            ('paypal_token_gec', orm['zobpress.BoardPayPal:paypal_token_gec']),
            ('paypal_payer_id', orm['zobpress.BoardPayPal:paypal_payer_id']),
        ))
        db.send_create_signal('zobpress', ['BoardPayPal'])
        
        # Adding model 'Job'
        db.create_table('zobpress_job', (
            ('id', orm['zobpress.Job:id']),
            ('board', orm['zobpress.Job:board']),
            ('name', orm['zobpress.Job:name']),
            ('category', orm['zobpress.Job:category']),
            ('is_active', orm['zobpress.Job:is_active']),
            ('is_expired', orm['zobpress.Job:is_expired']),
            ('is_editable', orm['zobpress.Job:is_editable']),
            ('password', orm['zobpress.Job:password']),
            ('paypal_token_sec', orm['zobpress.Job:paypal_token_sec']),
            ('paypal_token_gec', orm['zobpress.Job:paypal_token_gec']),
            ('created_on', orm['zobpress.Job:created_on']),
            ('updated_on', orm['zobpress.Job:updated_on']),
        ))
        db.send_create_signal('zobpress', ['Job'])
        
        # Adding model 'Category'
        db.create_table('zobpress_category', (
            ('id', orm['zobpress.Category:id']),
            ('board', orm['zobpress.Category:board']),
            ('name', orm['zobpress.Category:name']),
            ('slug', orm['zobpress.Category:slug']),
        ))
        db.send_create_signal('zobpress', ['Category'])
        
        # Creating unique_together for [job_form, order] on JobFieldModel.
        db.create_unique('zobpress_jobfieldmodel', ['job_form_id', 'order'])
        
        # Creating unique_together for [job_form, name] on JobFieldModel.
        db.create_unique('zobpress_jobfieldmodel', ['job_form_id', 'name'])
        
    
    
    def backwards(self, orm):
        
        # Deleting unique_together for [job_form, name] on JobFieldModel.
        db.delete_unique('zobpress_jobfieldmodel', ['job_form_id', 'name'])
        
        # Deleting unique_together for [job_form, order] on JobFieldModel.
        db.delete_unique('zobpress_jobfieldmodel', ['job_form_id', 'order'])
        
        # Deleting model 'Board'
        db.delete_table('zobpress_board')
        
        # Deleting model 'JobFile'
        db.delete_table('zobpress_jobfile')
        
        # Deleting model 'JobFieldModel'
        db.delete_table('zobpress_jobfieldmodel')
        
        # Deleting model 'JobData'
        db.delete_table('zobpress_jobdata')
        
        # Deleting model 'JobFormModel'
        db.delete_table('zobpress_jobformmodel')
        
        # Deleting model 'BoardExtendedSettings'
        db.delete_table('zobpress_boardextendedsettings')
        
        # Deleting model 'BoardPayments'
        db.delete_table('zobpress_boardpayments')
        
        # Deleting model 'BoardPayPal'
        db.delete_table('zobpress_boardpaypal')
        
        # Deleting model 'Job'
        db.delete_table('zobpress_job')
        
        # Deleting model 'Category'
        db.delete_table('zobpress_category')
        
    
    
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
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
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
            'Meta': {'unique_together': "(('job_form', 'order'), ('job_form', 'name'))"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'job_form': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['zobpress.JobFormModel']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'order': ('django.db.models.fields.IntegerField', [], {}),
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
        }
    }
    
    complete_apps = ['zobpress']
