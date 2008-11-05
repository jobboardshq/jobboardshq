from django import forms

from zobpress.models import Board
from django.conf import settings

class ManageSettingsForm(forms.ModelForm):
    
    class Meta:
        model = Board
        exclude = ('board', 'subdomain', 'owner')
        
    def save(self, *args, **kwargs):
        "Save the board, add the given domain to webfaction."
        super(ManageSettingsForm, self).save(*args, **kwargs)
        if not settings.WEBFACTION_DEBUG:
            import xmlrpclib
            server = xmlrpclib.Server('https://api.webfaction.com/')
            session_id, account = server.login('zobpress', '4db69244')
            server.create_domain(session_id, 'example.com', 'www')

    
    