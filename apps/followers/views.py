from django.db.models import F, Count
from rest_framework.viewsets import ModelViewSet

from apps.followers.models import Follower
from apps.followers.serializers import FollowerModelSerializer


class FollowerModelViewSet(ModelViewSet):
    """View set for model follower"""

    serializer_class = FollowerModelSerializer
    queryset = Follower.objects.all().annotate(
        follower_name=F('follower__username')
    )

    def get_queryset(self):
        """Get only your followers"""

        queryset = self.queryset.filter(owner=self.request.user)
        return queryset
