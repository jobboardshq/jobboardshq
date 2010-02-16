
from django import forms

from zobpress.forms import JobStaticForm, JobContactForm, get_job_form
from zobpress.models import Applicant, Category, JobType


class ApplyForm(forms.ModelForm):
    
    class Meta:
        model = Applicant
        exclude = ["board", "job"]
        
    def __init__(self, board,*args, **kwargs):
        self.board = board
        super(ApplyForm, self).__init__(*args, **kwargs)
    

class AdvancedSearchForm(forms.Form):
    def __init__(self, board, *args, **kwargs):
        self.board = board
        super(AdvancedSearchForm, self).__init__(*args, ** kwargs)
        self.fields['category'] = forms.ModelChoiceField(queryset=Category.objects.filter(board=self.board), required=False)
        self.fields['job_type'] = forms.ModelChoiceField(queryset=JobType.objects.filter(board=self.board), required=False)
        
    q = forms.CharField(label='Search for', max_length=80, required=False)
    
    def clean(self):
        if (self.cleaned_data['q'] == '') and (self.cleaned_data['category'] == self.cleaned_data['job_type'] == None):
            raise forms.ValidationError('Please specify any of the criteria for search results.')
        return self.cleaned_data