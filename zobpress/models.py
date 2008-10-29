from django.db import models
from django.db.models import permalink
from django import forms
from django.conf import settings

type_mapping = {
                'CharField':(forms.CharField, dict(max_length = 100)), 'TextField': (forms.CharField, dict(widget = forms.Textarea)), 'BooleanField':(forms.BooleanField, dict(required = False)),
                'URLField': (forms.URLField, dict()), 'EmailField': (forms.EmailField, dict()),
                'CategoryField': (forms.ModelChoiceField, dict()), 'FileField':(forms.FileField, dict()), 
                }
rev_type_mapping_list  = [(v[0], k) for k,v in type_mapping.iteritems()]
rev_type_mapping = {}
for el in rev_type_mapping_list:
    rev_type_mapping[el[0]] = el[1]


class Board(models.Model):
    subdomain = models.CharField(max_length = 100)
    name = models.CharField(max_length = 100)
    description = models.TextField()
    
    def __unicode__(self):
        return self.name
    
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
        
    
class Employee(models.Model):
    board = models.ForeignKey(Board)
    name = models.CharField(max_length = 100)
    category = models.ForeignKey(Category, null = True, blank = True)
    
    is_editable = models.BooleanField(default = False)
    
    created_on = models.DateTimeField(auto_now_add = 1)
    updated_on = models.DateTimeField(auto_now = 1)
    
    @permalink
    def get_absolute_url(self):
        return ('zobpress.views.person', [str(self.id)])
    
    def as_snippet(self):
        "Get the current job as a snippet."
        snippet = ""
        data = self.employeedata_set.all()[:2]
        for datum in data:
            snippet += "%s: %s" % (datum.name, datum.value)
            snippet += '\n'
        return snippet

    
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
    
class Job(models.Model):
    board = models.ForeignKey(Board)
    name = models.CharField(max_length = 100)
    category = models.ForeignKey(Category, null = True, blank = True)
    is_editable = models.BooleanField(default = False)
    
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
    uploaded_file = models.FileField(upload_to = 'jobfiles/')
    public_path = models.CharField(max_length = 100)
    content_type = models.CharField(max_length = 100)
    
    def get_absolute_url(self):
        return settings.MEDIA_URL + self.public_path
    
class EmployeeFile(models.Model):
    "Files attached to a specific Job"
    employee = models.ForeignKey(Employee)
    employee_data = models.ForeignKey(EmployeeData)
    uploaded_file = models.FileField(upload_to = 'employeefiles/')
    public_path = models.CharField(max_length = 100)
    content_type = models.CharField(max_length = 100)
    
    def get_absolute_url(self):
        return settings.MEDIA_URL + self.public_path