from django import forms

from zobpress.models import Board
from django.conf import settings

class ManageSettingsForm(forms.ModelForm):
    
    class Meta:
        model = Board
        exclude = ('board', 'subdomain', 'owner')
        
    def save(self, *args, **kwargs):
        "Save the board, add the given domain to webfaction."
        import pdb
        pdb.set_trace()
        board = super(ManageSettingsForm, self).save(*args, **kwargs)
        site = self.cleaned_data['domain']
        bits_len = len(site.split('.'))
        if not bits_len == 3:
            pass #Raise exception etc
        subdomain = site.split('.')[0]
        domain = '.'.join(site.split('.')[1:])
        if not settings.WEBFACTION_DEBUG:
            import xmlrpclib
            server = xmlrpclib.Server('https://api.webfaction.com/')
            session_id, account = server.login('zobpress', '4db69244')
            server.create_domain(session_id, domain, subdomain)
        return board

    
    