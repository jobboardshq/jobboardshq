from django.db import models

class ContactedPeople(models.Model):
    "People who have contacted us."
    name = models.CharField(max_length = 100)
    email = models.EmailField()
    phone_number = models.CharField(max_length = 100)
    url = models.URLField()
    
    query = models.TextField()
    
    
    

