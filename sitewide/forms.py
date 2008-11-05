from django import forms
from django.forms import ValidationError

from zobpress.models import Board
from registration.forms import RegistrationForm

class NewBoardForms(RegistrationForm):
    subdomain = forms.CharField(max_length = 100)
    name = forms.CharField(max_length = 100)
    description = forms.CharField(widget = forms.Textarea)
    #email = forms.EmailField()
    
    def clean_subdomain(self):
        try:
            Board.objects.get(subdomain = self.cleaned_data['subdomain'])
        except Board.DoesNotExist:
            return self.cleaned_data['subdomain']
        raise ValidationError('This subdomain is already taken. Please choose another.')
    
    def save(self, *args, **kwargs):
        user = super(NewBoardForms, self).save(*args, **kwargs)
        return Board.objects.register_new_board(subdomain = self.cleaned_data['subdomain'], name=self.cleaned_data['name'], description= self.cleaned_data['description'], user = user)
        