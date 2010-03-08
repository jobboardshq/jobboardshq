from django import forms
from django.forms import ValidationError
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.conf import settings

import random

from emailsubs.models import EmailSubscription

class EmailCaptureForm(forms.Form):
    email = forms.EmailField()
    
    def __init__(self, board, *args, **kwargs):
        super(EmailCaptureForm, self).__init__(*args, **kwargs)
        self.board = board
    
    def clean_email(self):
        try:
            EmailSubscription.objects.get(board = self.board, email = self.cleaned_data['email'])
        except EmailSubscription.DoesNotExist:
            return self.cleaned_data['email']
        raise ValidationError('This email is already registered.')
        
    def save(self):
        email_sub = EmailSubscription(board = self.board, email = self.cleaned_data['email'],)
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
    from django.contrib.sites.models import Site
    site = Site.objects.get_current()
    return 'http://%s.%s/' % (board.subdomain, site.domain)#TODO