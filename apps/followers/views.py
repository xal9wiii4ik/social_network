from rest_framework.viewsets import ModelViewSet

from apps.followers.models import Follower
from apps.followers.serializers import FollowerModelSerializer


class FollowerModelViewSet(ModelViewSet):
    """View set for model follower"""

    serializer_class = FollowerModelSerializer
    queryset = Follower.objects.all()
