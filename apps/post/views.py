from rest_framework.viewsets import ModelViewSet

from apps.post.models import Post, Subject
from apps.post.serializers import SubjectModelSerializer, PostModelSerializer


class SubjectModelViewSet(ModelViewSet):
    """Model view set for subject"""

    queryset = Subject.objects.all()
    serializer_class = SubjectModelSerializer


class PostModelViewSet(ModelViewSet):
    """Model view set for post"""

    queryset = Post.objects.all()
    serializer_class = PostModelSerializer
