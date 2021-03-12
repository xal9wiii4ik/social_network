from rest_framework import serializers

from apps.post.models import (
    Post,
    Subject,
    Comment,
    LikeDislike,
)


class SubjectModelSerializer(serializers.ModelSerializer):
    """Model serializer for subject"""

    class Meta:
        model = Subject
        fields = '__all__'


class PostModelSerializer(serializers.ModelSerializer):
    """Model serializer for post"""

    comments = serializers.SerializerMethodField()
    number_likes = serializers.SerializerMethodField()
    number_dislikes = serializers.SerializerMethodField()
    username = serializers.CharField(read_only=True)
    post_count = serializers.IntegerField(read_only=True)
    image_url = serializers.SerializerMethodField()
    is_owner = serializers.BooleanField(read_only=True)
    user_id = serializers.IntegerField(read_only=True)

    def get_image_url(self, obj):
        if obj.image:
            return obj.image.url
        return ''

    def get_number_likes(self, obj):
        """Func for getting number of likes"""

        return len(LikeDislike.objects.filter(post_id=obj.id, like=1))

    def get_number_dislikes(self, obj):
        """Func for getting number of dislikes"""

        return len(LikeDislike.objects.filter(post_id=obj.id, dislike=1))

    def get_comments(self, obj):
        """Func for getting comments to post"""

        queryset = Comment.objects.filter(post_id=obj.id, parent=None)
        serializer = CommentModelSerializer(queryset, many=True)
        return serializer.data

    class Meta:
        model = Post
        fields = '__all__'


class LikeDislikeModelSerializer(serializers.ModelSerializer):
    """Model serializer for like and dislike"""

    class Meta:
        model = LikeDislike
        fields = '__all__'


class CommentModelSerializer(serializers.ModelSerializer):
    """Model serializer for comments"""

    child = serializers.SerializerMethodField()

    def get_child(self, obj):
        """Func for getting kids to this comment"""

        queryset = Comment.objects.filter(parent_id=obj.id)
        serializer = CommentModelSerializer(queryset, many=True)
        return serializer.data

    class Meta:
        model = Comment
        fields = '__all__'
