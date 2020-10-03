from django.db import models

# Create your models here.
from account.models import User, Service


class Trade(models.Model):
    parties = models.ManyToManyField(to=User)
    service = models.ForeignKey(to=Service, on_delete=models.SET_NULL, null=True)


class Step(models.Model):
    name = models.CharField(max_length=64, default='')
    created_date = models.DateTimeField(auto_now_add=True)
    duration = models.IntegerField(default=24)
    given_stock = models.CharField(max_length=64, default='')
    got_stock = models.CharField(max_length=64, default='')
    trade = models.ForeignKey(to='Trade', on_delete=models.CASCADE, related_name='steps')


class Condition(models.Model):
    title = models.CharField(max_length=32, default='')
    description = models.CharField(max_length=32, default='')
    checked = models.BooleanField(default=False)
    related_round = models.ForeignKey(to='Step', on_delete=models.CASCADE, related_name='conditions')
