from django.contrib import admin

from apps.post.models import Subject, Post, Comment


@admin.register(Subject)
class SubjectModelAdmin(admin.ModelAdmin):
    """Model admin for subject"""

    list_display = ['id', 'subject']


@admin.register(Comment)
class CommentModelAdmin(admin.ModelAdmin):
    """Model admin for comment"""

    list_display = ['id', 'username', 'title', 'text', 'date']

    def username(self, obj):
        return obj.user.username

    def title(self, obj):
        return obj.post.title


@admin.register(Post)
class PostModelAdmin(admin.ModelAdmin):
    """Model admin for post"""

    list_display = ['id', 'owner', 'subject', 'title', 'published_date']
    list_filter = ['published_date']
    # TODO: check list_display_links
