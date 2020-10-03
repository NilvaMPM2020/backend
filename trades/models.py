from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.
from account.models import User, Service


class Trade(models.Model):
    class StatusChoices(models.IntegerChoices):
        ACTIVE = 0, _('active')
        WAITING_FOR_CANCELLATION_APPROVAL = 1, _('waiting for cancellation approval')
        JUDGEMENT = 2, _('judgement')
        CANCELLED = 3, _('cancelled')

    parties = models.ManyToManyField(to=User)
    service = models.ForeignKey(to=Service, on_delete=models.SET_NULL, null=True)
    status = models.IntegerField(choices=StatusChoices.choices, default=StatusChoices.ACTIVE)


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
    related_step = models.ForeignKey(to='Step', on_delete=models.CASCADE, related_name='conditions')


class Judge(models.Model):
    class DecisionChoices(models.IntegerChoices):
        FIRST_PARTY = 0, _('first party')
        SECOND_PARTY = 1, _('second party')

    trade = models.ForeignKey(to='Trade', on_delete=models.CASCADE, related_name='judgements')
    judge = models.ForeignKey(to=User, on_delete=models.CASCADE)
    decision = models.IntegerField(choices=DecisionChoices.choices)
