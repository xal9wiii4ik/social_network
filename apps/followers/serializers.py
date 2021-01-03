from rest_framework import serializers

from apps.followers.models import Follower


class FollowerModelSerializer(serializers.ModelSerializer):
    """Serializer for model follower"""

    class Meta:
        model = Follower
        fields = '__all__'
