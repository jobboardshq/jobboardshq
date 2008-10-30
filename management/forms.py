from django import forms

from zobpress.models import Board

class ManageSettingsForm(forms.ModelForm):
    
    class Meta:
        model = Board
        exclude = ('board', 'subdomain', 'owner')
    
    