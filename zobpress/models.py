from django.db import models
from django.db.models import permalink
from django import forms
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.sites.models import Site

from django.template.defaultfilters import slugify
from libs.fields import AutoSlugField

import random
from datetime import date, timedelta

type_mapping = {
                'CharField':(forms.CharField, dict(max_length = 100)), 'TextField': (forms.CharField, dict(widget = forms.Textarea)), 'BooleanField':(forms.BooleanField, dict(required = False)),
                'URLField': (forms.URLField, dict()), 'EmailField': (forms.EmailField, dict()),
                'CategoryField': (forms.ModelChoiceField, dict()), 'FileField':(forms.FileField, dict()), 
                }
rev_type_mapping_list  = [(v[0], k) for k,v in type_mapping.iteritems()]
rev_type_mapping = {}
for el in rev_type_mapping_list:
    rev_type_mapping[el[0]] = el[1]
    
class BoardManager(models.Manager):
    "Manager for a board."
    def register_new_board(self, subdomain, name, description, user):
        "Create a new board, creating other objects as needed."
        board = Board(subdomain = subdomain, name = name, description = description, owner = user)
        board.save()
        from emailsubs.models import EmailSent
        email_sent = EmailSent(board =  board)
        email_sent.save()
        from profiles.models import UserProfile
        user_profile = UserProfile(user = user)
        user_profile.save()
        board_extended_settings = BoardExtendedSettings(board = board)
        board_extended_settings.save()
        JobFormModel.objects.create_default_form(board = board)
        return board

class Board(models.Model):
    subdomain = models.CharField(max_length = 100, unique = True)
    domain = models.CharField(null = True, blank = True, max_length = 100, unique = True)
    name = models.CharField(max_length = 100)
    description = models.TextField()
    
    #Settings for Board
    "For listings value  of 0 means it never expires. For cost 0 means listing is free."
    job_listing_expires = models.PositiveIntegerField(default = 0)#Number of days a job should show up before being removed.
    cost_per_job_listing = models.PositiveIntegerField(default = 0)#Amount in USD which a user needs to pay to activate their listing.
    
    owner = models.ForeignKey(User)
    
    objects = BoardManager()
    
    def get_absolute_url(self):
        current_site = Site.objects.get_current()
        return 'http://%s.%s' % (self.subdomain, current_site.domain)
    
    def __unicode__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        # create settings
        BoardSettings.objects.create(board=self)
        super(Board, self).save(*args, **kwargs)
    
class BoardSettings(models.Model):
    analytics_code = models.TextField(null=True, blank=True)
    keywords = models.TextField(null=True, blank=True)
    tag_line = models.CharField(max_length = 250, null=True, blank=True)
    template = models.CharField(max_length = 100, default='default')
    board = models.OneToOneField(Board, related_name='settings')
    
class BoardPayPal(models.Model):
    board = models.OneToOneField(Board, primary_key = True)
    paypal_token_sec = models.CharField(null = True, blank = True, max_length = 100)
    paypal_token_gec = models.CharField(null = True, blank = True, max_length = 100)
    paypal_payer_id = models.CharField(null = True, blank = True, max_length = 100)
    
class BoardExtendedSettings(models.Model):
    "Extended settings for the board"
    board = models.OneToOneField(Board, primary_key = True)
    is_default_job_form = models.BooleanField(True)#Is the Job form a Default form.
    
class BoardPaymentsManager(models.Manager):
    def add_job_payment(self, board, amount, amount_for = None):
        if amount_for == None:
            amount_for = date.today()
        board_payment, created = BoardPayments.objects.get_or_create(board = board,  amount_for = amount_for)
        board_payment.job_payments = board_payment.job_payments + amount
        board_payment.save()
        
class BoardPayments(models.Model):
    board = models.ForeignKey(Board)
    amount_for = models.DateField()
    job_payments = models.PositiveIntegerField(default = 0, )
    payment_type = models.CharField(default = 'PayPal', max_length = 10)# As we get multiple gateways, we will have multiple types.
    
    created_on = models.DateTimeField(auto_now_add = 1)
    updated_on = models.DateTimeField(auto_now_add = 1)
    
    objects = BoardPaymentsManager()
    
class Category(models.Model):
    "Categories for a specific board"
    board = models.ForeignKey(Board)
    name = models.CharField(max_length = 100)
    slug = models.SlugField(max_length = 100)
    
    @models.permalink
    def get_absolute_url(self):
        return('zobpress.views.category_jobs', [self.slug])
    
    @models.permalink
    def get_jobs_url(self):
        return('zobpress.views.category_jobs', [self.slug])
    
    def __unicode__(self):
        return self.name
    
class JobType(models.Model):
    board = models.ForeignKey(Board)
    name = models.CharField(max_length = 100)
    slug = AutoSlugField(max_length = 100)
    
    def __unicode__(self):
        return self.name
    
    
class JobFormModelManager(models.Manager):
    def create_default_form(self, board):
        job_form = JobFormModel(board = board)
        job_form.save()
        job_description = JobFieldModel(job_form = job_form, name = 'Job Description', type = 'TextField', order = 0)
        job_description.save()

class JobFormModel(models.Model):
    "Model for Job form for a specific Job board."
    board = models.ForeignKey(Board, unique = True)
    
    objects = JobFormModelManager()
    
    def __unicode__(self):
        return self.board.name
    
class JobFieldModel(models.Model):
    "Model for Job form fields for a specific Job board."
    job_form = models.ForeignKey(JobFormModel)
    name = models.CharField(max_length = 100)
    type = models.CharField(max_length = 100)
    order = models.IntegerField()
    
    def __unicode__(self):
        return self.job_form.board.name
    
    class Meta:
        unique_together = (('job_form', 'order'), ('job_form', 'name'))
        ordering = ('-order', )

class JobPublicManager(models.Manager):
    def get_query_set(self):
        return super(JobPublicManager, self).get_query_set().filter(is_active = True)
        
    def get_public_jobs(self, board):
        "If people_listing_expires is a non zero value, filter on number of days this will be active. Else all paid for are active."
        active_for = board.job_listing_expires
        if active_for:
            return self.filter(created_on__gt = date.today() - timedelta(days = active_for))
        else:
            return self.all()
    
class Job(models.Model):
    board = models.ForeignKey(Board)
    name = models.CharField(max_length = 100, null=True, blank=True)
    category = models.ForeignKey(Category, null = True, blank = True)
    job_type = models.ForeignKey(JobType, null=True, blank=True)
    job_slug = models.SlugField(max_length=100)
    
    is_active = models.BooleanField(default = False)#listings start as inactive. After Payment become active.
    is_expired = models.BooleanField(default = False)#Has this listing expired yet?
    is_editable = models.BooleanField(default = False)
    password = models.CharField(max_length = 100, null = True, blank = True)
    paypal_token_sec = models.CharField(max_length = 100,  null = True, blank = True)#Token returned from set_express_checkout
    paypal_token_gec = models.CharField(max_length = 100,  null = True, blank = True)#Token returned from get_express_checkout
    
    objects = models.Manager()
    public_objects = JobPublicManager()
    
    created_on = models.DateTimeField(auto_now_add = 1)
    updated_on = models.DateTimeField(auto_now = 1)
    
    def __unicode__(self):
        return self.name or ''
    
    def as_snippet(self):
        "Get the current job as a snippet."
        snippet = ""
        data = self.jobdata_set.all()[:2]
        for datum in data:
            snippet += "%s: %s" % (datum.name, datum.value)
            snippet += '\n'
        return snippet
   
    @property
    def as_clob(self):
        "As a large text."
        snippet = ""
        snippet += '\n'.join([self.name or '', self.category or '', self.job_type or ''])
        data = self.jobdata_set.all()
        for datum in data:
            snippet += "%s: %s" % (datum.name, datum.value)
            snippet += '\n'
        return snippet
    
    @permalink
    def get_absolute_url(self):
        return ('zobpress.views.job', [str(self.job_slug)])
    
    class Meta:
        ordering = ('-created_on', )
    
    def save(self, *args, **kwargs):
        self.job_slug = slugify(self.name)
        slug_count = Job.objects.filter(job_slug__icontains = self.job_slug).count()
        if slug_count:
            self.job_slug += str(slug_count + 1)
        super(Job, self).save(*args, **kwargs)
        
class JobData(models.Model):
    job = models.ForeignKey(Job)
    data_type = models.CharField(max_length = 100)
    name = models.CharField(max_length = 100)
    value = models.TextField()
    
    def value_as_str(self):
        "Value as pretty string"
        if self.data_type == 'BooleanField':
            if self.value:
                return 'Yes'
            else:
                return 'No'
        return self.value

    def get_absolute_url(self):
        if self.data_type == 'FileField':
            return self.jobfile_set.all()[0].get_absolute_url()
        return self.value
    
class JobFile(models.Model):
    "Files attached to a specific Job"
    job = models.ForeignKey(Job)
    job_data = models.ForeignKey(JobData)
    uploaded_file = models.CharField(max_length = 100)
    public_path = models.CharField(max_length = 100)
    content_type = models.CharField(max_length = 100)
    
    def get_absolute_url(self):
        return settings.MEDIA_URL + self.public_path
    
class Page(models.Model):
    title = models.CharField(max_length=100)
    page_slug = models.SlugField(max_length=100)
    content = models.TextField()
    job_board = models.ForeignKey(Board)
    
    def __unicode__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        # TODO: validate the page_slug value
        super(Page, self).save(*args, **kwargs)