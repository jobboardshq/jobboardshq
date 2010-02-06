from django import forms
from django.forms import ValidationError
from django.conf import settings
from django.template.loader import render_to_string

from zobpress.models import Board
from registration.forms import RegistrationForm
from django.core.mail import send_mail

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
        
 