# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Changing field 'Board.introductory_text'
        db.alter_column('zobpress_board', 'introductory_text', self.gf('django.db.models.fields.TextField')(null=True))


    def backwards(self, orm):
        
        # Changing field 'Board.introductory_text'
        db.alter_column('zobpress_board', 'introductory_text', self.gf('django.db.models.fields.TextField')())


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
        'zobpress.applicant': {
            'Meta': {'object_name': 'Applicant'},
            'board': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['zobpress.Board']"}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'job': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['zobpress.Job']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'response': ('django.db.models.fields.TextField', [], {}),
            'resume': ('django.db.models.fields.files.FileField', [], {'max_length': '100'})
        },
        'zobpress.board': {
            'Meta': {'object_name': 'Board'},
            'cost_per_job_listing': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'domain': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '100', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'introductory_text': ('django.db.models.fields.TextField', [], {'default': "''", 'null': 'True', 'blank': 'True'}),
            'job_listing_expires': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'subdomain': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'template': ('django.db.models.fields.TextField', [], {'default': "'frontend/css/template2.css'", 'max_length': '128'})
        },
        'zobpress.boardextendedsettings': {
            'Meta': {'object_name': 'BoardExtendedSettings'},
            'board': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['zobpress.Board']", 'unique': 'True', 'primary_key': 'True'}),
            'is_default_job_form': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'zobpress.boardpayments': {
            'Meta': {'object_name': 'BoardPayments'},
            'amount_for': ('django.db.models.fields.DateField', [], {}),
            'board': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['zobpress.Board']"}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': '1', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'job_payments': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'payment_type': ('django.db.models.fields.CharField', [], {'default': "'PayPal'", 'max_length': '10'}),
            'updated_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': '1', 'blank': 'True'})
        },
        'zobpress.boardpaypal': {
            'Meta': {'object_name': 'BoardPayPal'},
            'board': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['zobpress.Board']", 'unique': 'True', 'primary_key': 'True'}),
            'paypal_payer_id': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'paypal_token_gec': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'paypal_token_sec': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        'zobpress.boardsettings': {
            'Meta': {'object_name': 'BoardSettings'},
            'allow_public_posting': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'analytics_code': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'board': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'settings'", 'unique': 'True', 'to': "orm['zobpress.Board']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'keywords': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'logo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'tag_line': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'template': ('django.db.models.fields.CharField', [], {'default': "'default'", 'max_length': '100'})
        },
        'zobpress.category': {
            'Meta': {'unique_together': "(('board', 'name', 'is_deleted'),)", 'object_name': 'Category'},
            'board': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['zobpress.Board']"}),
            'category_count': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '100', 'db_index': 'True'})
        },
        'zobpress.deletedentities': {
            'Meta': {'ordering': "['-deleted_on']", 'object_name': 'DeletedEntities'},
            'board': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['zobpress.Board']"}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'deleted_on': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        'zobpress.job': {
            'Meta': {'ordering': "('-created_on',)", 'object_name': 'Job'},
            'board': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['zobpress.Board']"}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['zobpress.Category']"}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': '1', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_default': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_editable': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_expired': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'job_slug': ('django.db.models.fields.SlugField', [], {'max_length': '100', 'db_index': 'True'}),
            'job_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['zobpress.JobType']", 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '300', 'null': 'True', 'blank': 'True'}),
            'paypal_token_gec': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'paypal_token_sec': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'times_viewed': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'updated_on': ('django.db.models.fields.DateTimeField', [], {'auto_now': '1', 'blank': 'True'})
        },
        'zobpress.jobcontactdetail': {
            'Meta': {'object_name': 'JobContactDetail'},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'job': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['zobpress.Job']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        'zobpress.jobdata': {
            'Meta': {'object_name': 'JobData'},
            'data_type': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'job': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['zobpress.Job']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'value': ('django.db.models.fields.TextField', [], {})
        },
        'zobpress.jobfieldmodel': {
            'Meta': {'ordering': "('-order',)", 'unique_together': "(('job_form', 'name'),)", 'object_name': 'JobFieldModel'},
            'help_text': ('django.db.models.fields.TextField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'job_form': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['zobpress.JobFormModel']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '10'}),
            'required': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'zobpress.jobfile': {
            'Meta': {'object_name': 'JobFile'},
            'content_type': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'job': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['zobpress.Job']"}),
            'job_data': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['zobpress.JobData']"}),
            'public_path': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'uploaded_file': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'zobpress.jobformmodel': {
            'Meta': {'object_name': 'JobFormModel'},
            'board': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['zobpress.Board']", 'unique': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'zobpress.jobtype': {
            'Meta': {'object_name': 'JobType'},
            'board': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['zobpress.Board']"}),
            'count': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique_with': '()', 'max_length': '100', 'populate_from': 'None', 'db_index': 'True'})
        },
        'zobpress.page': {
            'Meta': {'unique_together': "(('board', 'page_slug'),)", 'object_name': 'Page'},
            'board': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['zobpress.Board']"}),
            'content': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'page_slug': ('django.db.models.fields.SlugField', [], {'max_length': '100', 'db_index': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['zobpress']
