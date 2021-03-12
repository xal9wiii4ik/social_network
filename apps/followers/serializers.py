from rest_framework import serializers

from apps.followers.models import Follower


class FollowerModelSerializer(serializers.ModelSerializer):
    """Serializer for model follower"""

    follower_name = serializers.CharField(read_only=True)

    class Meta:
        model = Follower
        fields = ['owner', 'follower', 'follower_name']
