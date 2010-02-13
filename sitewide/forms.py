
import re

from django import forms
from django.forms import ValidationError
from django.conf import settings
from django.template.loader import render_to_string

from zobpress.models import Board
from registration.forms import RegistrationForm
from django.core.mail import send_mail
from registration.models import RegistrationProfile

class NewBoardForms(RegistrationForm):
    subdomain = forms.CharField(max_length = 100, help_text="The subdomain you want. Eg, if you want nurses.jobboardshq.com enter nurses here.")
    name = forms.CharField(max_length = 100, help_text="The name of your job board, eg The nurses job board.")
    description = forms.CharField(widget = forms.Textarea, help_text="Describe your jobboard. This is used at various places like meta keywords.")
    #email = forms.EmailField()
    
    def __init__(self, subdomain = None, *args, **kwargs):
        super(NewBoardForms, self).__init__(*args, **kwargs)
        self.fields["subdomain"].initial = subdomain
        
    
    def clean_subdomain(self):
        if self.cleaned_data['subdomain'] in settings.UNALLOWED_SUBDOMAINS:
            raise ValidationError('This subdomain name is reserved. Please choose another.')
        
        if not re.match(r'^[a-z0-9-]+$', self.cleaned_data['subdomain'].lower()):
            raise ValidationError('subdomain can have only a-z, 0-9, -')
        
        try:
            Board.objects.get(subdomain__iexact = self.cleaned_data['subdomain'])
        except Board.DoesNotExist: #@UndefinedVariable
            return self.cleaned_data['subdomain']
        raise ValidationError('This subdomain is already taken. Please choose another.')
    
    def save(self, profile_callback=None):
        data = self.cleaned_data
        username = data["username"]
        password = data["password1"]
        #user = super(NewBoardForms, self).save(*args, **kwargs)
        #Return the username password so the user can be logged in in the next step.
        subdomain = self.cleaned_data['subdomain']
        new_user = RegistrationProfile.objects.create_inactive_user(username=self.cleaned_data['username'],
                                                                    password=self.cleaned_data['password1'],
                                                                    email=self.cleaned_data['email'],
                                                                    subdomain=subdomain,
                                                                    profile_callback=profile_callback)
        user =  new_user
        return Board.objects.register_new_board(subdomain = self.cleaned_data['subdomain'], name=self.cleaned_data['name'], description= self.cleaned_data['description'], user = user), username, password
        
        
from sitewide.models import ContactedPeople




class ContactUsForm(forms.ModelForm):
    def save(self, *args, **kwargs):
        super(ContactUsForm, self).save(*args, **kwargs)
        #Email now.
        subject = render_to_string("sitewide/emails/contact_subject.txt")
        message = render_to_string("sitewide/emails/contact_message.txt")
        from_email = settings.ADMINS[0][1]
        recipient_list = [el[1] for el in settings.ADMINS]
        send_mail(subject, message, from_email, recipient_list, fail_silently =False)
        
    
    class Meta:
        model = ContactedPeople
        
 
