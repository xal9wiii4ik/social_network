from django.contrib import admin

from apps.post.models import Subject, Post, Comment, LikeDislike


@admin.register(Subject)
class SubjectModelAdmin(admin.ModelAdmin):
    """Model admin for subject"""

    list_display = ['id', 'subject']


@admin.register(LikeDislike)
class LikeDislikeModelAdmin(admin.ModelAdmin):
    """Model admin for like and dislike"""

    list_display = ['id', 'get_username', 'get_title', 'like', 'dislike']

    def get_username(self, obj):
        return obj.user.username

    def get_title(self, obj):
        return obj.post.title


@admin.register(Comment)
class CommentModelAdmin(admin.ModelAdmin):
    """Model admin for comment"""

    list_display = ['id', 'get_username', 'get_title', 'text', 'date']

    def get_username(self, obj):
        return obj.user.username

    def get_title(self, obj):
        return obj.post.title


@admin.register(Post)
class PostModelAdmin(admin.ModelAdmin):
    """Model admin for post"""

    list_display = ['id', 'owner', 'subject', 'title', 'published_date']
    list_filter = ['published_date']
