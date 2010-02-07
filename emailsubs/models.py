from django.db import models

from zobpress.models import Board, BoardSpecificEntities
import datetime

class EmailSubscription(BoardSpecificEntities):
    "Emails subscribed to a board"
    email = models.EmailField()
    is_confirmed = models.BooleanField(default = False)
    key = models.CharField(max_length = 100) #Generated random key, to validate confirm/unsubscribe
    
    created_on = models.DateTimeField(default = datetime.datetime.now)
    is_active = models.BooleanField(default = True)
    
    def __unicode__(self):
        return self.email
    
    class Meta:
        unique_together = (("board", "email"))
    
class EmailSent(BoardSpecificEntities):
    "Last time emails were sent out for a specific board"
    num_times_sent = models.PositiveIntegerField(default = 0)
    created_on =  models.DateTimeField(auto_now_add = 1)
    updated_on =  models.DateTimeField(auto_now = 1)
    
    def __unicode__(self):
        return self.board.name