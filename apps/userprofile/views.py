from django.contrib.auth import get_user_model

from rest_framework import permissions
from rest_framework.viewsets import mixins, GenericViewSet

from apps.userprofile.serializers import (
    AbstractUserOwnerModelSerializer,
    AbstractUserGuestsModelSerializer,
)
from apps.userprofile.permissions import IsOwner


class AbstractUserOwnerViewSet(mixins.RetrieveModelMixin,
                               mixins.DestroyModelMixin,
                               mixins.UpdateModelMixin,
                               GenericViewSet):
    """View set for owner of abstract user"""

    serializer_class = AbstractUserOwnerModelSerializer
    queryset = get_user_model().objects.all()
    permission_classes = [IsOwner]


class AbstractUserGuestsViewSet(mixins.ListModelMixin,
                                mixins.RetrieveModelMixin,
                                GenericViewSet):
    """View set for guests of abstract user"""

    serializer_class = AbstractUserGuestsModelSerializer
    queryset = get_user_model().objects.all()
    permission_classes = [permissions.IsAuthenticated]
