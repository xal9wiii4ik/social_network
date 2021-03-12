from django.contrib.auth import get_user_model
from django.test import TestCase

from apps.post.models import Subject, Comment, Post, LikeDislike
from apps.post.serializers import (
    SubjectModelSerializer,
    PostModelSerializer,
    LikeDislikeModelSerializer,
    CommentModelSerializer,
)


class SubjectModelSerializerTestCase(TestCase):
    """Test case for Subject Model Serializer"""

    def test_ok(self):
        subject_1 = Subject.objects.create(subject='subject_1')
        subject_2 = Subject.objects.create(subject='subject_2')

        subjects = Subject.objects.all()
        data = SubjectModelSerializer(subjects, many=True).data
        expected_data = [
            {
                'id': subject_1.id,
                'subject': 'subject_1'
            },
            {
                'id': subject_2.id,
                'subject': 'subject_2'
            }
        ]
        self.assertEqual(first=expected_data, second=data)


class PostModelSerializerTestCase(TestCase):
    """Test case for Subject Model Serializer"""

    def test_ok(self):
        user = get_user_model().objects.create(username='user', is_active=True)
        subject = Subject.objects.create(subject='subject')
        post = Post.objects.create(subject=subject, owner=user, title='post', body='body')

        data = PostModelSerializer(post).data
        data.pop('published_date')
        expected_data = {
            'id': post.id,
            'comments': [],
            'number_likes': 0,
            'number_dislikes': 0,
            'image_url': '',
            'title': 'post',
            'body': 'body',
            'image': None,
            'owner': user.id,
            'subject': subject.id
        }
        self.assertEqual(first=expected_data, second=data)


class CommentModelSerializerTestCase(TestCase):
    """Test case for Comment Model Serializer"""

    def test_ok(self):
        user = get_user_model().objects.create(username='user', is_active=True)
        subject = Subject.objects.create(subject='subject')
        post = Post.objects.create(subject=subject, owner=user, title='title', body='body')
        comment = Comment.objects.create(user=user, post=post, text='parent')
        comment_child = Comment.objects.create(user=user, post=post, text='child', parent=comment)

        data = CommentModelSerializer(comment).data
        data.pop('date')
        data['child'][0].pop('date')
        expected_data = {
            'id': comment.id,
            'child': [
                {
                    'id': comment_child.id,
                    'child': [],
                    'text': 'child',
                    'user': user.id,
                    'post': post.id,
                    'parent': comment.id
                }
            ],
            'text': 'parent',
            'user': user.id,
            'post': post.id,
            'parent': None
        }
        self.assertEqual(first=expected_data, second=data)


class LikeDislikeModelSerializerTestCase(TestCase):
    """Test case for LikeDislike Model Serializer"""

    def test_ok(self):
        user = get_user_model().objects.create(username='user', is_active=True)
        subject_1 = Subject.objects.create(subject='subject_1')
        subject_2 = Subject.objects.create(subject='subject_2')
        post_1 = Post.objects.create(subject=subject_1, owner=user, title='title', body='body')
        post_2 = Post.objects.create(subject=subject_2, owner=user, title='title', body='body')

        like_dislike_1 = LikeDislike.objects.create(user=user, post=post_1, like=1)
        like_dislike_2 = LikeDislike.objects.create(user=user, post=post_2, dislike=1)
        likes_dislikes = LikeDislike.objects.all()

        data = LikeDislikeModelSerializer(likes_dislikes, many=True).data
        expected_data = [
            {
                'id': like_dislike_1.id,
                'user': user.id,
                'post': post_1.id,
                'like': 1,
                'dislike': 0
            },
            {
                'id': like_dislike_2.id,
                'user': user.id,
                'post': post_2.id,
                'like': 0,
                'dislike': 1
            }
        ]
        self.assertEqual(first=expected_data, second=data)
