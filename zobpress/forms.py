
#import random
#from copy import copy
from os.path import join
import os

from django import forms
from django.conf import settings

from marcofucci_utils import fields as marcofucci_fields

from zobpress.models import BoardSettings, type_mapping, rev_type_mapping,\
    JobContactDetail, Board
from zobpress.models import JobFormModel, JobFieldModel, JobType
from zobpress.models import Job, JobData, Category, JobFile, Page

class PageForm(forms.ModelForm):
    content = forms.CharField(widget = forms.Textarea(attrs = {"class": "RTEField"}))
    class Meta:
        model = Page
        exclude = ('board',)

class TemplateForm(forms.Form):
    
    #To add a new template just update a new dictionary under.
    template_choices = ({'css':'frontend/css/template1.css',
                         'image':'frontend/images/blue_theme.gif',
                         'name':'Theme Water'
                         },
                        {'css':'frontend/css/template2.css',
                         'image':'frontend/images/brown_theme.gif',
                         'name': 'Theme Earth'
                         },
                        {'css':'frontend/css/template3.css',
                         'image':'frontend/images/classic_theme.gif',
                         'name':'Theme Fire'}
                        )
    widget_choices = [(el['css'],el['name']) for el in template_choices]
    template = forms.ChoiceField(choices=widget_choices,widget=forms.RadioSelect)
    
    def save(self,board):
        board.template = self.cleaned_data['template']
        board.save()
        

        
        
        
class BoardEditForm(forms.ModelForm):
    class Meta:
        model = Board
        fields = ("name", "description")

from form_utils.fields import ClearableFileField
from form_utils.widgets import ImageWidget
        
class BoardSettingsForm(forms.ModelForm):
    
    logo = ClearableFileField(file_field=forms.ImageField(widget=ImageWidget,required=False))
    
    class Meta:
        model = BoardSettings
        exclude = ('board', 'template')
        
class BoardDomainForm(forms.ModelForm):
    
    def __init__(self, board, *args, **kwargs):
        self.board = board
        super(BoardDomainForm, self).__init__(*args, **kwargs)
        
    class Meta:
        model = Board
        fields = ('domain',)

    def save(self, commit=True):
        self.board.domain = self.cleaned_data['domain']
        if commit:
            self.board.save()
        return self.board
        
class JobStaticForm(forms.ModelForm):    
    name = forms.CharField(widget = forms.TextInput(attrs={"class" : "textinput",  "size":"50"},))
    description = forms.CharField(widget = forms.Textarea(attrs={"class": "richtext", "cols" : 60, "rows":25}))
    job_type = forms.ModelChoiceField(queryset = JobType.objects.all(), widget=forms.RadioSelect, empty_label = None)
    category = forms.ModelChoiceField(queryset = Category.objects.all(), widget=forms.RadioSelect, empty_label = None)
    
    def __init__(self, board, *args, **kwargs):
        super(JobStaticForm, self).__init__(*args, **kwargs)
        self.board = board
        self.fields["job_type"].queryset = JobType.objects.filter(board = self.board)
        self.fields["category"].queryset = Category.objects.filter(board = self.board)
        
        
    def save(self, *args, **kwargs):
        job = super(JobStaticForm, self).save(commit = False)
        job.board = self.board
        return super(JobStaticForm, self).save(*args, **kwargs)
        
    
    class Meta:
        model = Job
        fields = ('name', 'description', 'category', 'job_type')
    
def get_job_form(board, job = None, return_job_fields_also = False, captcha_required=True):
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
                    data_type = rev_type_mapping[self.fields[field].__class__]
                    value = self.cleaned_data[field]
                    if not value:
                        continue
                    job_data = JobData(job = job, name = field, value = value)
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
        setattr(JobForm, field.name.strip(), get_field_type(field, board))
    
    if captcha_required:
        # recaptcha field
        setattr(JobForm, 'recaptcha', marcofucci_fields.ReCaptchaField())
    
    if return_job_fields_also:
        return type('JobForm', (forms.Form, ), dict(JobForm.__dict__)), job_fields
    else:
        return type('JobForm', (forms.Form, ), dict(JobForm.__dict__))
    

def get_field_type(field, board):
    data_type = field.type
    field_class, kwargs = type_mapping.get(data_type, (forms.CharField, {}))
    kwargs['required'] = field.required
    kwargs['help_text'] = field.help_text
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
        exclude = ["board", "category_count", "is_deleted"]
        
    def __init__(self, board, *args, **kwargs):
        super(CategoryForm, self).__init__(*args, **kwargs)
        self.board = board
        
        
    def clean_name(self):
        data = self.cleaned_data
        try:
            Category.objects.get(name =  data["name"], board = self.board)
            raise forms.ValidationError("This name is already taken. Please choose another.")
        except Category.DoesNotExist:
            return data["name"]
        
class JobTypeForm(forms.ModelForm):
    def __init__(self, board, *args, **kwargs):
        super(JobTypeForm, self).__init__(*args, **kwargs)
        self.board = board
        
    class Meta:
        model = JobType
        fields = ["name"]
                
    
class JobFieldEditForm(forms.ModelForm):
    class Meta:
        model = JobFieldModel
        fields =  ["name", "type", "required"]
        
class JobContactForm(forms.ModelForm):
    class Meta:
        model = JobContactDetail
        fields = ["name", "email", "website"]
        
        
    
     
#class PasswordForm(forms.Form):
#    password = forms.CharField(widget = forms.PasswordInput(attrs = {'size':50}), help_text = 'Enter the passwords assocoiated with this posting. Not required, but allows you to edit the posting later.')
#    
#    def save(self):
#        return self.cleaned_data['password']
#    
    
    