from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet, mixins, GenericViewSet

from apps.post.models import Post, Subject, Comment
from apps.post.serializers import (
    SubjectModelSerializer,
    PostModelSerializer,
    CommentModelSerializer
)
from apps.post.permissions import IsOwnerOrReadOnly, IsOwnerOrStaff


class SubjectModelViewSet(ModelViewSet):
    """Model view set for subject"""

    queryset = Subject.objects.all()
    serializer_class = SubjectModelSerializer
    permission_classes = [permissions.IsAdminUser,]


class PostModelViewSet(ModelViewSet):
    """Model view set for post"""

    queryset = Post.objects.all()
    serializer_class = PostModelSerializer
    permission_classes = [IsOwnerOrReadOnly,]

    def perform_create(self, serializer):
        serializer.validated_data['owner'] = self.request.user
        serializer.save()


class CommentModelViewSet(ModelViewSet):
    """Model View Set for comments"""

    queryset = Comment.objects.all()
    serializer_class = CommentModelSerializer
    permission_classes = [IsOwnerOrStaff,]

    def get_queryset(self):
        print(self.request)
        print(self.request.__dict__)
        return self.queryset.filter(user_id=self.request._user)

    def perform_create(self, serializer):
        serializer.validated_data['user'] = self.request.user
        serializer.save()
