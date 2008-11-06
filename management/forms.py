from django import forms

from zobpress.models import Board
from django.conf import settings
from django.forms import ValidationError

class ManageSettingsForm(forms.ModelForm):
    
    class Meta:
        model = Board
        exclude = ('board', 'subdomain', 'owner')
        
    def __init__(self, board, *args, **kwargs):
        self.board = board
        super(ManageSettingsForm, self).__init__(*args, **kwargs)
        
    def clean_domain(self):
        "You must be a paying customer to be able to use Domain"
        if self.cleaned_data['domain']:
            if not self.board.owner.get_profile().is_paid:
                raise ValidationError('You need to upgrade to a paid account to be able to use a custom domain.')
        return self.cleaned_data['domain']
        
    def save(self, *args, **kwargs):
        "Save the board, add the given domain to webfaction."
        board = super(ManageSettingsForm, self).save(*args, **kwargs)
        site = self.cleaned_data['domain']
        bits_len = len(site.split('.'))
        if not bits_len == 3:
            pass #Raise exception etc
        subdomain = site.split('.')[0]
        domain = '.'.join(site.split('.')[1:])
        if settings.WEBFACTION_SERVER:
            import xmlrpclib
            server = xmlrpclib.Server('https://api.webfaction.com/')
            session_id, account = server.login('zobpress', '4db69244')
            server.create_domain(session_id, domain, subdomain)
        return board

    
    