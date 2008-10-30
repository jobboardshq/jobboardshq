from django import forms
from django.forms import ValidationError
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.conf import settings

import random

from emailsubs.models import EmailSubscription

class EmailCaptureForm(forms.Form):
    email = forms.EmailField()
    send_jobs_email = forms.BooleanField(required = False)
    send_employee_email = forms.BooleanField(required = False)
    
    def __init__(self, board, *args, **kwargs):
        super(EmailCaptureForm, self).__init__(*args, **kwargs)
        self.board = board
    
    def clean_email(self):
        try:
            EmailSubscription.objects.get(board = self.board, email = self.cleaned_data['email'])
        except EmailSubscription.DoesNotExist:
            return self.cleaned_data['email']
        raise ValidationError('This email is already registered for this board.')
        
    def save(self):
        email_sub = EmailSubscription(board = self.board, email = self.cleaned_data['email'], send_jobs_email= self.cleaned_data['send_jobs_email'], send_employee_email=self.cleaned_data['send_employee_email'])
        random_key = ''.join([random.choice('012345678') for el in  range(10)])
        email_sub.key = random_key
        email_sub.save()
        site_root = get_site_root(self.board)
        payload = {'email_sub':email_sub, 'site_root':site_root}
        email_text = render_to_string('emailsubs/confirm_mail.txt', payload)
        subject = 'Please confirm your email'
        send_mail(subject, email_text, settings.EMAIL_SENDER,
            [email_sub.email], fail_silently=False)
        return email_sub
    
def get_site_root(board):
    return 'http://%s.shabda.tld:8000' % (board.subdomain)#TODO