from rest_framework import serializers

from apps.post.models import Post, Subject


class SubjectModelSerializer(serializers.ModelSerializer):
    """Model serializer for subject"""

    class Meta:
        model = Subject
        fields = '__all__'


class PostModelSerializer(serializers.ModelSerializer):
    """Model serializer for post"""

    class Meta:
        model = Post
        fields = '__all__'
