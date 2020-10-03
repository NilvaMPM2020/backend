from django.contrib import admin

# Register your models here.
from trades.models import Trade, Step, Condition, Judge


@admin.register(Trade)
class TradeAdmin(admin.ModelAdmin):
    list_display = ('service', 'status')


@admin.register(Step)
class StepAdmin(admin.ModelAdmin):
    list_display = ('name', 'duration', 'trade', 'given_stock', 'got_stock')


@admin.register(Condition)
class ConditionAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'checked', 'related_step')


@admin.register(Judge)
class JudgeAdmin(admin.ModelAdmin):
    list_display = ('trade', 'judge', 'decision')
