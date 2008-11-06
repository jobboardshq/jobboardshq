from django.db import models
from django.contrib.auth.models import User

from zobpress.models import Board

#The various payment plans
payment_plans = ['20USDPM']

class UserProfile(models.Model):
    "Profiles for users"
    user = models.ForeignKey(User)
    payer_id = models.CharField(max_length = 100, null = True, blank = True)
    trx_id = models.CharField(max_length = 100, null = True, blank = True)
    referrer = models.CharField(max_length = 100, null = True, blank = True)
    is_paid = models.BooleanField(default = False)
    payment_plan = models.CharField(default = payment_plans[0], max_length = 100)
    
    def get_board(self):
        return Board.objects.get(owner = self.user)
    
    

    
