from django.db import models
from django.contrib.auth.models import User
from .constants import GENDER_TYPE 

# Create your models here.
class UserAccount(models.Model):
    user= models.OneToOneField(User, related_name='account', on_delete= models.CASCADE )
    birth_date = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_TYPE)
    balance = models.DecimalField(default=0, max_digits=12, decimal_places=2)

    def __str__(self):
        return self.user.username
    

    