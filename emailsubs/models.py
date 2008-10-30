from django.db import models

from zobpress.models import Board

class EmailSubscription(models.Model):
    "Emails subscribed to a board"
    board = models.ForeignKey(Board)
    email = models.EmailField(unique = True)
    send_jobs_email = models.BooleanField(default = True)
    send_employee_email = models.BooleanField(default = True)
    is_confirmed = models.BooleanField(default = False)
    key = models.CharField(max_length = 100) #Genrated random key, to validate confirm/unsubscribe
    
class EmailSent(models.Model):
    "Last time emails were sent out for a sepcific board"
    board = models.ForeignKey(Board, unique = True)
    num_times_sent = models.PositiveIntegerField(default = 0)
    
    created_on =  models.DateTimeField(auto_now_add = 1)
    updated_on =  models.DateTimeField(auto_now = 1)
    
    def __unicode__(self):
        return self.board