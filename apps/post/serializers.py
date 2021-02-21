from rest_framework import serializers

from apps.post.models import Post, Subject, Comment


class SubjectModelSerializer(serializers.ModelSerializer):
    """Model serializer for subject"""

    class Meta:
        model = Subject
        fields = '__all__'


class PostModelSerializer(serializers.ModelSerializer):
    """Model serializer for post"""

    comments = serializers.SerializerMethodField()

    def get_comments(self, obj):
        """Func for getting comments to post"""

        queryset = Comment.objects.filter(post_id=obj.id, parent=None)
        serializer = CommentModelSerializer(queryset, many=True)
        return serializer.data

    class Meta:
        model = Post
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
