from django.db import models

from zobpress.models import Board

class EmailSubs(models.Model):
    "Emails subscribed to a board"
    board = models.ForeignKey(Board)
    email = models.EmailField()
    send_jobs_email = models.BooleanField(default = True)
    send_employee_email = models.BooleanField(default = True)
    
class EmailSent(models.Model):
    "Last time emails were sent out for a sepcific board"
    board = models.ForeignKey(Board)
    num_times_sent = models.PositiveIntegerField(default = 0)
    
    created_on =  models.DateTimeField(auto_now_add = 1)
    updated_on =  models.DateTimeField(auto_now = 1)