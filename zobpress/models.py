from django.db import models
from django.db.models import permalink
from django import forms

type_mapping = {'CharField':forms.CharField(max_length = 100), 'TextField': forms.CharField(widget = forms.Textarea), 'BooleanField':forms.BooleanField(),
                'URLField': forms.URLField(), 'EmailField': forms.EmailField()
                }

class Board(models.Model):
    subdomain = models.CharField(max_length = 100)
    name = models.CharField(max_length = 100)
    description = models.TextField()
    
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
    
    created_on = models.DateTimeField(auto_now_add = 1)
    updated_on = models.DateTimeField(auto_now = 1)
    
    @permalink
    def get_absolute_url(self):
        return ('zobpress.views.person', [str(self.id)])
    
class EmployeeData(models.Model):
    employee = models.ForeignKey(Employee)
    name = models.CharField(max_length = 100)
    value = models.TextField()
    
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
    
    created_on = models.DateTimeField(auto_now_add = 1)
    updated_on = models.DateTimeField(auto_now = 1)
    
    @permalink
    def get_absolute_url(self):
        return ('zobpress.views.job', [str(self.id)])
    
class JobData(models.Model):
    job = models.ForeignKey(Job)
    name = models.CharField(max_length = 100)
    value = models.TextField()