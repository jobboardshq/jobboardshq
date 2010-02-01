from django import forms
from django.forms import ValidationError
from django.conf import settings

from zobpress.models import Board
from registration.forms import RegistrationForm

class NewBoardForms(RegistrationForm):
    subdomain = forms.CharField(max_length = 100)
    name = forms.CharField(max_length = 100)
    description = forms.CharField(widget = forms.Textarea)
    #email = forms.EmailField()
    
    def clean_subdomain(self):
        if self.cleaned_data['subdomain'] in settings.UNALLOWED_SUBDOMAINS:
            raise ValidationError('This subdomain name is reserved. Please choose another.')
        try:
            Board.objects.get(subdomain = self.cleaned_data['subdomain'])
        except Board.DoesNotExist: #@UndefinedVariable
            return self.cleaned_data['subdomain']
        raise ValidationError('This subdomain is already taken. Please choose another.')
    
    def save(self, *args, **kwargs):
        user = super(NewBoardForms, self).save(*args, **kwargs)
        return Board.objects.register_new_board(subdomain = self.cleaned_data['subdomain'], name=self.cleaned_data['name'], description= self.cleaned_data['description'], user = user)
        