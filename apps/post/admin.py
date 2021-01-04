from django.contrib import admin

from apps.post.models import Subject, Post


@admin.register(Subject)
class SubjectModelAdmin(admin.ModelAdmin):
    """Model admin for subject"""

    list_display = ['id', 'subject']


@admin.register(Post)
class PostModelAdmin(admin.ModelAdmin):
    """Model admin for post"""

    list_display = ['id', 'owner', 'subject', 'title', 'published_date']
    list_filter = ['published_date']
    # TODO: check list_display_links
