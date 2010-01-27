from django import forms
from django.conf import settings

#import random
#from copy import copy
from os.path import join
import os

from zobpress.models import BoardSettings, type_mapping, rev_type_mapping
from zobpress.models import JobFormModel, JobFieldModel, JobType
from zobpress.models import Job, JobData, Category, JobFile, Page

class PageForm(forms.ModelForm):
    
    class Meta:
        model = Page
        exclude = ('job_board',)
    
    
class BoardSettingsForm(forms.ModelForm):
    
    class Meta:
        model = BoardSettings
        exclude = ('board',)
        
class JobStaticForm(forms.ModelForm):    
    name = forms.CharField(widget = forms.TextInput(attrs={"class" : "textinput"}))
    job_type = forms.ModelChoiceField(queryset = JobType.objects.all(), widget=forms.RadioSelect, empty_label = None)
    category = forms.ModelChoiceField(queryset = Category.objects.all(), widget=forms.RadioSelect, empty_label = None)
    
    def __init__(self, board, *args, **kwargs):
        super(JobStaticForm, self).__init__(*args, **kwargs)
        self.board = board
        
    def save(self, *args, **kwargs):
        job = super(JobStaticForm, self).save(commit = False)
        job.board = self.board
        return super(JobStaticForm, self).save(*args, **kwargs)
        
    
    class Meta:
        model = Job
        fields = ('name', 'category', 'job_type')
    
def get_job_form(board, job = None, return_job_fields_also = False):
    """Return the Job form for a specific Board."""
    job_form = JobFormModel.objects.get(board = board)
    job_fields = JobFieldModel.objects.filter(job_form = job_form).order_by('order')
    class JobForm(forms.Form):
        def __init__(self, *args, **kwargs):
            forms.Form.__init__(self, *args, **kwargs)
            self.board = board
            self.job = job
            if job and job.jobdata_set.count():
                for datum in job.jobdata_set.all():
                    try:
                        self.fields[datum.name].initial = datum.value
                    except KeyError:
                        pass  
        def save(self):
                job = self.job
                if not job:
                    job = Job(board = self.board)
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
    # setattr(JobForm, 'name', forms.CharField(max_length = 100))
    for field in job_fields:
        setattr(JobForm, field.name.strip(), get_field_type(field.type, board))
    if return_job_fields_also:
        return type('JobForm', (forms.Form, ), dict(JobForm.__dict__)), job_fields
    else:
        return type('JobForm', (forms.Form, ), dict(JobForm.__dict__))
    

def get_field_type(data_type, board):
    field_class, kwargs = type_mapping.get(data_type, (forms.CharField, {}))
    if data_type == 'CategoryField':
        kwargs['queryset'] = Category.objects.filter(board = board)
    return field_class(**kwargs)

class IndeedSearchForm(forms.Form):
    # publisher_id = forms.CharField()
    q = forms.CharField(label=u'what', required=False)
    l = forms.CharField(label=u'where', required=False)
    
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        exclude = ["board"]
    
    
     
#class PasswordForm(forms.Form):
#    password = forms.CharField(widget = forms.PasswordInput(attrs = {'size':50}), help_text = 'Enter the passwords assocoiated with this posting. Not required, but allows you to edit the posting later.')
#    
#    def save(self):
#        return self.cleaned_data['password']
#    
    
    