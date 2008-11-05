from django.db import models
from django.contrib.auth.models import User

from zobpress.models import Board

class UserProfile(models.Model):
    "Profiles for users"
    user = models.ForeignKey(User)
    payer_id = models.CharField(max_length = 100, null = True, blank = True)
    trx_id = models.CharField(max_length = 100, null = True, blank = True)
    referrer = models.CharField(max_length = 100, null = True, blank = True)
    
    def get_board(self):
        return Board.objects.get(owner = self.user)
    
    

    
