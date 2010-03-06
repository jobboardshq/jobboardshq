from django.db import models

class ContactedPeople(models.Model):
    "People who have contacted us."
    name = models.CharField(max_length = 100,blank=True,null=True)
    email = models.EmailField(blank=True,null=True,help_text='So that we may get back to you.')
    phone_number = models.CharField(max_length = 100,blank=True,null=True,help_text='If you would have us call you.')
    url = models.URLField(blank=True,null=True,help_text='Not really required. But let us know more about you.')
    query = models.TextField(blank=True,null=True,help_text='How can we help you?')
    