from django.contrib.auth.models import AbstractUser
from django.core.files.storage import FileSystemStorage
from django.db import models
from django.utils.translation import gettext_lazy as _

fs = FileSystemStorage(location='static')
imgFs = FileSystemStorage(location='static/img')


# Create your models here.

class User(AbstractUser):
    class TypeChoices(models.IntegerChoices):
        REGULAR = 0, _('regular')
        BUSINESS = 1, _('business')

    name = models.CharField(max_length=64, default='کاربر')
    phone = models.CharField(max_length=11)
    email = models.EmailField(default='')
    avatar = models.ImageField(storage=imgFs, null=True, default=None)
    rate = models.FloatField(default=0)
    enabled = models.BooleanField(default=True)
    user_type = models.IntegerField(choices=TypeChoices.choices, default=TypeChoices.REGULAR)


class Service(models.Model):
    name = models.CharField(max_length=64, default='', db_index=True)
    avatar = models.ImageField(storage=imgFs, null=True, default=None)
    description = models.CharField(max_length=256, default='')
    business = models.ForeignKey(to='User', on_delete=models.CASCADE)


class Round(models.Model):
    name = models.CharField(max_length=64, default='')
    duration = models.IntegerField(default=24)
    given_stock = models.CharField(max_length=64, default='')
    got_stock = models.CharField(max_length=64, default='')
    service = models.ForeignKey(to='Service', on_delete=models.CASCADE, related_name='rounds')


class ConditionSchema(models.Model):
    title = models.CharField(max_length=32, default='')
    description = models.CharField(max_length=32, default='')
    checked = models.BooleanField(default=False)
    related_round = models.ForeignKey(to='Round', on_delete=models.CASCADE, related_name='conditions')

