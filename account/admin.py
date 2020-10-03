from django.contrib import admin

# Register your models here.
from account.models import User, Service, Round, ConditionSchema
from trades.models import Condition


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'name', 'phone', 'avatar', 'user_type', 'rate')


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'business')


@admin.register(Round)
class RoundAdmin(admin.ModelAdmin):
    list_display = ('name', 'duration', 'service', 'given_stock', 'got_stock')


@admin.register(ConditionSchema)
class ConditionAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'checked', 'related_round')
