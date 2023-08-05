
from unicodedata import decimal
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
        user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
        name = models.CharField(max_length=200, blank=True, null=True)
        balance = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
        investment_wallet =models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
        withdrawal_wallet =models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
        country = models.CharField(max_length=200, null=True, blank=True)
        vidCount = models.IntegerField(default=0, blank=True,null=True)
        watchAt =models.DateTimeField(auto_now_add=False, blank=True,null=True)
        dailyLimit=models.IntegerField(default=0, blank=True,null=True)
        createdAt = models.DateTimeField(auto_now_add=True)
        _id = models.AutoField(primary_key=True, editable=False)

        def __str__(self):
            return self.name

    
class Investment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    plan = models.CharField(max_length=200, null=True, blank=True)
    amount = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    percentage=models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    interest = models.DecimalField(max_digits=7,default=0, decimal_places=2, null=True, blank=True)
    duration = models.IntegerField(default=0,null=True,blank=True)
    completed = models.BooleanField(default=False)
    createdAt = models.DateTimeField(auto_now_add=True)
    endAt =  models.DateTimeField(auto_now_add=False,null=True, blank=True)
    _id = models.AutoField(primary_key=True, editable=False)

    def __str__(self):
        return self.plan

class Deposit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    amount = models.DecimalField(max_digits=7,decimal_places=2,null=True)
    is_success = models.BooleanField(default=False)
    paidAt = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    _id = models.AutoField(primary_key=True, editable=False)

    def __str__(self):
        return self.name


    



class withdrawal(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    name =  models.CharField(max_length=200, blank=True, null=True)
    amount = models.DecimalField( max_digits=7, decimal_places=2,null=True, blank=True)
    accountName = models.CharField(max_length=200, null=True, blank=True)
    accountBank_Name = models.CharField(max_length=200, null=True, blank=True)
    accountBank_Number = models.IntegerField(null=True, blank=True)
    is_success = models.BooleanField(default=False)
    createdAt = models.DateTimeField(auto_now_add=True)
    _id = models.AutoField(primary_key=True, editable=False)

    def __str__(self):
        return self.name  


