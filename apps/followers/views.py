from django.contrib.auth import get_user_model
from django.db.models import F

from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.viewsets import mixins, GenericViewSet

from apps.followers.models import Follower
from apps.followers.serializers import FollowerModelSerializer
from apps.followers.permissions import IsOwnerOrIsAuthenticated

class FollowerModelViewSet(mixins.ListModelMixin,
                           mixins.CreateModelMixin,
                           mixins.DestroyModelMixin,
                           GenericViewSet):
    """View set for model follower"""

    serializer_class = FollowerModelSerializer
    queryset = Follower.objects.all().annotate(
        follower_name=F('follower__username')
    )
    permission_classes = [IsOwnerOrIsAuthenticated]

    def get_queryset(self):
        """Get only user followers"""

        queryset = self.queryset.filter(owner=self.request.user)
        return queryset

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            self.queryset.get(follower=serializer.validated_data['follower'], owner=request.user)
            return Response({'error': 'you already follow'}, status=status.HTTP_400_BAD_REQUEST)
        except:
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def destroy(self, request, *args, **kwargs):
        try:
            user = get_user_model().objects.get(id=request.parser_context['kwargs']['pk'])
            instance = self.queryset.get(follower=user, owner=request.user)
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        """Add owner"""

        serializer.validated_data['owner'] = self.request.user
        serializer.save()
