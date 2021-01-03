from django.contrib import admin

from apps.followers.models import Follower


@admin.register(Follower)
class FollowerModelAdmin(admin.ModelAdmin):
    """Model follower in admin panel"""

    list_display = ['id', 'follower', 'owner']
