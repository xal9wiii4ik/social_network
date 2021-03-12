from django.db.models import F, Count
from rest_framework.decorators import action

from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, mixins, GenericViewSet
from rest_framework import status, parsers, renderers

from apps.post.models import (
    Post,
    Subject,
    Comment,
    LikeDislike,
)
from apps.post.serializers import (
    SubjectModelSerializer,
    PostModelSerializer,
    CommentModelSerializer,
    LikeDislikeModelSerializer,
)
from apps.post.permissions import IsOwnerOrReadOnly, IsOwnerOrStaffOrReadOnly, IsAdminOrReadOnly


class SubjectModelViewSet(mixins.ListModelMixin,
                          GenericViewSet):
    """Model view set for subject"""

    queryset = Subject.objects.all()
    serializer_class = SubjectModelSerializer
    permission_classes = [IsAdminOrReadOnly]


class PostModelViewSet(ModelViewSet):
    """Model view set for post"""

    queryset = Post.objects.all().annotate(
        username=F('owner__username'),
        post_count=Count('owner__post_owner'),
        user_id=F('owner__id')
    )
    serializer_class = PostModelSerializer
    permission_classes = [IsOwnerOrReadOnly]
    parser_classes = [parsers.MultiPartParser, parsers.JSONParser]

    def perform_create(self, serializer):
        serializer.validated_data['owner'] = self.request.user
        serializer.save()

    @action(detail=False, methods=['GET'], permission_classes=[permissions.IsAuthenticated])
    def my_posts(self, request):
        queryset = self.queryset.filter(owner=self.request.user)
        serializer = PostModelSerializer(queryset, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class LikeDislikeApiView(APIView):
    """Api view for model like and dislike"""

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, post_pk: str):
        try:
            queryset = LikeDislike.objects.get(post_id=post_pk, user=request.user)
            serializer = LikeDislikeModelSerializer(instance=queryset)
            request.data.pop('post')
            serializer.update(queryset, request.data)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except Exception:
            serializer = LikeDislikeModelSerializer(data=request.data)
            if serializer.is_valid():
                serializer.validated_data['user'] = request.user
                serializer.save()
            return Response(data={'create': 'Like or dislike was created'}, status=status.HTTP_201_CREATED)


class CommentModelViewSet(ModelViewSet):
    """Model View Set for comments"""

    queryset = Comment.objects.all()
    serializer_class = CommentModelSerializer
    permission_classes = [IsOwnerOrStaffOrReadOnly]

    def get_queryset(self):
        return self.queryset.filter(user_id=self.request.user)

    def perform_create(self, serializer):
        serializer.validated_data['user'] = self.request.user
        serializer.save()
