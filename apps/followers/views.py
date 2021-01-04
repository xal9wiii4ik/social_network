from django.db.models import F
from rest_framework.viewsets import ModelViewSet, mixins, GenericViewSet

from apps.followers.models import Follower, Subscriber
from apps.followers.serializers import FollowerModelSerializer, SubscribersModelSerializer


class FollowerModelViewSet(mixins.ListModelMixin,
                           mixins.DestroyModelMixin,
                           GenericViewSet):
    """View set for model follower"""

    serializer_class = FollowerModelSerializer
    queryset = Follower.objects.all().annotate(
        follower_name=F('follower__username')
    )

    def get_queryset(self):
        """Get only user followers"""

        queryset = self.queryset.filter(owner=self.request.user)
        return queryset


class SubscriberModelViewSet(mixins.ListModelMixin,
                             mixins.DestroyModelMixin,
                             GenericViewSet):
    """View set for model subscriber"""

    serializer_class = SubscribersModelSerializer
    queryset = Subscriber.objects.all().annotate(
        subscriber_name=F('subscriber__username')
    )

    def get_queryset(self):
        """Get only your subscribers"""

        queryset = self.queryset.filter(owner=self.request.user)
        return queryset
