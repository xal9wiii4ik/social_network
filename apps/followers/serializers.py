from rest_framework import serializers

from apps.followers.models import Follower, Subscriber


class FollowerModelSerializer(serializers.ModelSerializer):
    """Serializer for model follower"""

    follower_name = serializers.CharField(read_only=True)

    class Meta:
        model = Follower
        fields = ['owner', 'follower', 'follower_name']


class SubscribersModelSerializer(serializers.ModelSerializer):
    """Serializer for model subscriber"""

    subscriber_name = serializers.CharField(read_only=True)

    class Meta:
        model = Subscriber
        fields = ['owner', 'subscriber', 'subscriber_name']
