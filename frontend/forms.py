from zobpress.forms import JobStaticForm, JobContactForm, get_job_form
from django import forms
from zobpress.models import Applicant


class ApplyForm(forms.ModelForm):
    
    class Meta:
        model = Applicant
        exclude = ["board", "job"]
        
    def __init__(self, board,*args, **kwargs):
        self.board = board
        super(ApplyForm, self).__init__(*args, **kwargs)
    
    
    
    
