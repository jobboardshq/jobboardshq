from django import forms

from zobpress import models
from zobpress.models import Board, EmployeeFormModel, EmployeeFieldModel, type_mapping
from zobpress.models import Employee, EmployeeData
from zobpress.models import JobFormModel, JobFieldModel
from zobpress.models import Job, JobData

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
                    emp_data = EmployeeData(employee = employee, name = field, value = self.cleaned_data[field])
                    emp_data.save()
                return employee
    setattr(EmployeeForm, 'name', forms.CharField(max_length = 100))
    for field in employee_fields:
        setattr(EmployeeForm, field.name, type_mapping[field.type])#forms.CharField(max_length = 100))
    return type('EmployeeForm', (forms.Form, ), dict(EmployeeForm.__dict__))
    
def get_job_form(board):
    """Return the Job form for a specific Board."""
    job_form = JobFormModel.objects.get(board = board)
    job_fields = JobFieldModel.objects.filter(job_form = job_form).order_by('order')
    class JobForm(forms.Form):
        def __init__(self, *args, **kwargs):
            forms.Form.__init__(self, *args, **kwargs)
            self.board = board
        def save(self):
                job = Job(board = self.board, name = self.cleaned_data['name'])
                job.save()
                for field in self.cleaned_data.iterkeys():
                    if field in ['name']:
                        continue
                    job_data = JobData(job = job, name = field, value = self.cleaned_data[field])
                    job_data.save()
                return job
    setattr(JobForm, 'name', forms.CharField(max_length = 100))
    for field in job_fields:
        setattr(JobForm, field.name, type_mapping[field.type])
    return type('JobForm', (forms.Form, ), dict(JobForm.__dict__))
     
class PasswordForm(forms.Form):
    password = forms.CharField(widget = forms.PasswordInput(attrs = {'size':50}), help_text = 'Enter the passwords assocoiated with this posting.')
