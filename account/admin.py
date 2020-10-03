from django.contrib import admin

# Register your models here.
from account.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'name', 'phone', 'avatar', 'user_type', 'rate')

