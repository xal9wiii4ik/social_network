from django.contrib import admin

from apps.followers.models import Follower, Subscriber


@admin.register(Follower)
class FollowerModelAdmin(admin.ModelAdmin):
    """Model follower in admin panel"""

    list_display = ['id', 'owner', 'follower']


@admin.register(Subscriber)
class SubscriberModelAdmin(admin.ModelAdmin):
    """Model subscriber in admin panel"""

    list_display = ['id', 'owner', 'subscriber']
