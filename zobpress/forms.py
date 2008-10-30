from django import forms
from django.conf import settings

import random
from copy import copy
from os.path import join
import os

from zobpress import models
from zobpress.models import Board, EmployeeFormModel, EmployeeFieldModel, type_mapping, rev_type_mapping
from zobpress.models import Employee, EmployeeData, EmployeeFile
from zobpress.models import JobFormModel, JobFieldModel
from zobpress.models import Job, JobData, Category, JobFile

def get_employee_form(board):
    """Return the form for a specific Board."""
    employee_form = EmployeeFormModel.objects.get(board = board)
    employee_fields = EmployeeFieldModel.objects.filter(employee_form = employee_form).order_by('order')
    class EmployeeForm(forms.Form):
        def __init__(self, *args, **kwargs):
            forms.Form.__init__(self, *args, **kwargs)
            self.board = board
        def save(self):
                employee = Employee(board = self.board, name = self.cleaned_data['name'])
                employee.save()
                for field in self.cleaned_data.iterkeys():
                    if field in ['name']:
                        continue
                    data_type = rev_type_mapping[self.fields[field].__class__]
                    emp_data = EmployeeData(employee = employee, name = field, value = self.cleaned_data[field])
                    emp_data.data_type = data_type
                    emp_data.save()
                    if self.fields[field].__class__ == forms.ModelChoiceField:
                        if self.cleaned_data[field].__class__ == Category:
                            employee.category = self.cleaned_data[field]
                            employee.save()
                    if self.fields[field].__class__ == forms.FileField:
                        uploaded_file = self.cleaned_data[field]
                        upload_folder = join(settings.MEDIA_ROOT, board.subdomain, 'employee', employee.name)
                        try:
                            os.makedirs(upload_folder)
                        except OSError:
                            pass
                        path_to_upload = join(upload_folder, uploaded_file.name)
                        public_path = join(board.subdomain, 'employee', employee.name, uploaded_file.name)
                        out_file = open(path_to_upload, 'wb+')
                        for chunk in uploaded_file.chunks():
                            out_file.write(chunk)
                        out_file.close()
                        employee_file = EmployeeFile(employee = employee, uploaded_file = uploaded_file.name, public_path = public_path, content_type = uploaded_file.content_type)
                        employee_file.employee_data = emp_data
                        employee_file.save()
                return employee
    setattr(EmployeeForm, 'name', forms.CharField(max_length = 100))
    for field in employee_fields:
        setattr(EmployeeForm, field.name.strip(), get_field_type(field.type, board))
    return type('EmployeeForm', (forms.Form, ), dict(EmployeeForm.__dict__))
    
def get_job_form(board, job = None):
    """Return the Job form for a specific Board."""
    job_form = JobFormModel.objects.get(board = board)
    job_fields = JobFieldModel.objects.filter(job_form = job_form).order_by('order')
    class JobForm(forms.Form):
        def __init__(self, *args, **kwargs):
            forms.Form.__init__(self, *args, **kwargs)
            self.board = board
            self.job = job
        def save(self):
                job = self.job
                if not job:
                    job = Job(board = self.board, name = self.cleaned_data['name'])
                    job.save()
                else:
                    job.jobdata_set.all().delete()
                for field in self.cleaned_data.iterkeys():
                    if field in ['name']:
                        continue
                    data_type = rev_type_mapping[self.fields[field].__class__]
                    job_data = JobData(job = job, name = field, value = self.cleaned_data[field])
                    job_data.data_type = data_type
                    job_data.save()
                    if self.fields[field].__class__ == forms.ModelChoiceField:
                        if self.cleaned_data[field].__class__ == Category:
                            job.category = self.cleaned_data[field]
                            job.save()
                    if self.fields[field].__class__ == forms.FileField:
                        uploaded_file = self.cleaned_data[field]
                        upload_folder = join(settings.MEDIA_ROOT, board.subdomain, job.name)
                        try:
                            os.makedirs(upload_folder)
                        except OSError:
                            pass
                        path_to_upload = join(upload_folder, uploaded_file.name)
                        public_path = join(board.subdomain, job.name, uploaded_file.name)
                        out_file = open(path_to_upload, 'wb+')
                        for chunk in uploaded_file.chunks():
                            out_file.write(chunk)
                        out_file.close()
                        job_file = JobFile(job = job, uploaded_file = uploaded_file.name, public_path = public_path, content_type = uploaded_file.content_type)
                        job_file.job_data = job_data
                        job_file.save()
                return job
    setattr(JobForm, 'name', forms.CharField(max_length = 100))
    for field in job_fields:
        setattr(JobForm, field.name.strip(), get_field_type(field.type, board))
    return type('JobForm', (forms.Form, ), dict(JobForm.__dict__))
     
class PasswordForm(forms.Form):
    password = forms.CharField(widget = forms.PasswordInput(attrs = {'size':50}), help_text = 'Enter the passwords assocoiated with this posting. Not required, but allows you to edit the posting later.')
    
    def save(self):
        return self.cleaned_data['password']
    
def get_field_type(data_type, board):
    field_class, kwargs = type_mapping.get(data_type, (forms.CharField, {}))
    if data_type == 'CategoryField':
        kwargs['queryset'] = Category.objects.filter(board = board)
    return field_class(**kwargs)
