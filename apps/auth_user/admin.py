from django.contrib import admin

from apps.auth_user.models import Uid


@admin.register(Uid)
class UidAdmin(admin.ModelAdmin):
    list_display = ('uid', 'user')
