from django.db import models
from django.db.models import permalink
from django import forms
from django.conf import settings
from django.contrib.auth.models import User

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
        return board

class Board(models.Model):
    subdomain = models.CharField(max_length = 100)
    domain = models.CharField(null = True, blank = True, max_length = 100)
    name = models.CharField(max_length = 100)
    description = models.TextField()
    
    #Settings for Board
    "For listings value  of 0 means it never expires. For cost 0 means listing is free."
    job_listing_expires = models.PositiveIntegerField(default = 0)#Number of days a job should show up before being removed.
    people_listing_expires = models.PositiveIntegerField(default = 0)#Number of days a people should show up before being removed.
    cost_per_job_listing = models.PositiveIntegerField(default = 0)#Amount in USD which a user needs to pay to activate their listing.
    cost_per_people_listing = models.PositiveIntegerField(default = 0)#Amount in USD which a user needs to pay to activate their listing.
    
    owner = models.ForeignKey(User)
    
    objects = BoardManager()
    
    def get_absolute_url(self):
        return 'http://%s.shabda.tld:8000' % self.subdomain
    
    def __unicode__(self):
        return self.name
    
class BoardPaymentsManager(models.Manager):
    def add_job_payment(self, board, amount, amount_for = None):
        if amount_for == None:
            amount_for = date.today()
        board_payment, created = BoardPayments.objects.get_or_create(board = board,  amount_for = amount_for)
        board_payment.job_payments = board_payment.job_payments + amount
        board_payment.save()
        
    def add_employee_payments(self, board, amount, amount_for = None):
        if amount_for == None:
            amount_for = date.today()
        board_payment, created = BoardPayments.objects.get_or_create(board = board,  amount_for = amount_for)
        board_payment.employee_payments = board_payment.employee_payments + amount
        board_payment.save()
        
    
class BoardPayments(models.Model):
    board = models.ForeignKey(Board)
    amount_for = models.DateField()
    job_payments = models.PositiveIntegerField(default = 0, )
    employee_payments = models.PositiveIntegerField(default = 0)
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
    
    @models.permalink
    def get_people_url(self):
        return('zobpress.views.category_people', [self.slug])
    
    def __unicode__(self):
        return self.name
    
class EmployeeFormModel(models.Model):
    "Model for employee form for a specific Job board."
    board = models.ForeignKey(Board, unique = True)
    
    def __unicode__(self):
        return self.board.name
    
    
class EmployeeFieldModel(models.Model):
    "Model for employee form fields for a specific Job board."
    employee_form = models.ForeignKey(EmployeeFormModel)
    name = models.CharField(max_length = 100)
    type = models.CharField(max_length = 100)
    order = models.IntegerField()
    
    def __unicode__(self):
        return self.employee_form.board.name
    
    class Meta:
        unique_together = (('employee_form', 'order'), ('employee_form', 'name'))
        ordering = ('-order', )
        
class EmployeePublicManager(models.Manager):
    def get_query_set(self):
        return super(EmployeePublicManager, self).get_query_set().filter(is_active = True)
        
    def get_public_employees(self, board):
        "If people_listing_expires is a non zero value, filter on number of days this will be active. Else all paid for are active."
        active_for = board.people_listing_expires
        if active_for:
            return self.filter(created_on__gt = date.today() - timedelta(days = active_for))
        else:
            return self.all()
        
    
class Employee(models.Model):
    board = models.ForeignKey(Board)
    name = models.CharField(max_length = 100)
    category = models.ForeignKey(Category, null = True, blank = True)
    
    is_active = models.BooleanField(default = False)#listings start as inactive. After Payment become active.
    is_expired = models.BooleanField(default = False)#Has this listing expired yet?
    is_editable = models.BooleanField(default = False)
    password = models.CharField(max_length = 100, null = True, blank = True)
    paypal_token_sec = models.CharField(max_length = 100,  null = True, blank = True)#Token returned from set_express_checkout
    paypal_token_gec = models.CharField(max_length = 100,  null = True, blank = True)#Token returned from get_express_checkout
    
    created_on = models.DateTimeField(auto_now_add = 1)
    updated_on = models.DateTimeField(auto_now = 1)
    
    objects = models.Manager()
    public_objects = EmployeePublicManager()
    
    @permalink
    def get_absolute_url(self):
        return ('zobpress.views.person', [str(self.id)])
    
    def as_clob(self):
        "As a large text."
        snippet = ""
        data = self.employeedata_set.all()
        for datum in data:
            snippet += "%s: %s" % (datum.name, datum.value)
            snippet += '\n'
        return snippet

    
    def as_snippet(self):
        "Get the current job as a snippet."
        snippet = ""
        data = self.employeedata_set.all()[:2]
        for datum in data:
            snippet += "%s: %s" % (datum.name, datum.value)
            snippet += '\n'
        return snippet
    
    class Meta:
        ordering = ('-created_on', )

    
class EmployeeData(models.Model):
    employee = models.ForeignKey(Employee)
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
        try:
            if self.data_type == 'FileField':
                return self.employeefile_set.all()[0].get_absolute_url()
        except IndexError:
            pass
        return self.value
    
class JobFormModel(models.Model):
    "Model for Job form for a specific Job board."
    board = models.ForeignKey(Board, unique = True)
    
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
    name = models.CharField(max_length = 100)
    category = models.ForeignKey(Category, null = True, blank = True)
    
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
    
    def as_snippet(self):
        "Get the current job as a snippet."
        snippet = ""
        data = self.jobdata_set.all()[:2]
        for datum in data:
            snippet += "%s: %s" % (datum.name, datum.value)
            snippet += '\n'
        return snippet
    
    def as_clob(self):
        "As a large text."
        snippet = ""
        data = self.jobdata_set.all()
        for datum in data:
            snippet += "%s: %s" % (datum.name, datum.value)
            snippet += '\n'
        return snippet
    
    @permalink
    def get_absolute_url(self):
        return ('zobpress.views.job', [str(self.id)])
    
    class Meta:
        ordering = ('-created_on', )
    
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
    
class EmployeeFile(models.Model):
    "Files attached to a specific Job"
    employee = models.ForeignKey(Employee)
    employee_data = models.ForeignKey(EmployeeData)
    uploaded_file = models.CharField(max_length = 100)
    public_path = models.CharField(max_length = 100)
    content_type = models.CharField(max_length = 100)
    
    def get_absolute_url(self):
        return settings.MEDIA_URL + self.public_path