import json

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.db.models import F, Count

from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from apps.post.models import Subject, Post, LikeDislike, Comment
from apps.post.serializers import SubjectModelSerializer, PostModelSerializer, LikeDislikeModelSerializer


class SubjectApiTestCase(APITestCase):
    """Subject Api Test Case"""

    def setUp(self):
        password = make_password('password')
        url = reverse('token')

        self.user = get_user_model().objects.create(username='user',
                                                    password=password,
                                                    is_active=True,
                                                    is_staff=True)
        data = {
            'username': self.user.username,
            'password': 'password'
        }
        json_data = json.dumps(data)
        self.token = f"Token " \
                     f"{self.client.post(path=url, data=json_data, content_type='application/json').data['access']}"

        self.subject = Subject.objects.create(subject='subject')

    def test_list_authenticated(self):
        """Test for getting list with authenticated user"""

        url = reverse('subject-list')
        self.client.credentials(HTTP_AUTHORIZATION=self.token)
        response = self.client.get(path=url)
        subjects = Subject.objects.all()
        data = SubjectModelSerializer(subjects, many=True).data
        self.assertEqual(first=status.HTTP_200_OK, second=response.status_code)
        self.assertEqual(first=data, second=response.data)

    def test_list_un_authenticated(self):
        """Test for getting list with un authenticated user"""

        url = reverse('subject-list')
        response = self.client.get(path=url)
        self.assertEqual(first=status.HTTP_401_UNAUTHORIZED, second=response.status_code)


class PostApiTestCase(APITestCase):
    """Subject Api Test Case"""

    def setUp(self):
        password = make_password('password')
        url = reverse('token')

        self.user = get_user_model().objects.create(username='user',
                                                    password=password,
                                                    is_active=True,
                                                    is_staff=True)
        data = {
            'username': self.user.username,
            'password': 'password'
        }
        json_data = json.dumps(data)
        self.token = f"Token " \
                     f"{self.client.post(path=url, data=json_data, content_type='application/json').data['access']}"

        self.user_1 = get_user_model().objects.create(username='user_1',
                                                      password=password,
                                                      is_active=True,
                                                      is_staff=True)
        data_1 = {
            'username': self.user_1.username,
            'password': 'password'
        }
        json_data_1 = json.dumps(data_1)
        self.token_1 = f"Token " \
                       f"{self.client.post(path=url, data=json_data_1, content_type='application/json').data['access']}"

        self.subject = Subject.objects.create(subject='subject')

        self.post = Post.objects.create(subject=self.subject, owner=self.user, title='post', body='body')

    def test_list(self):
        """Test for getting list of posts"""

        url = reverse('post-list')
        response = self.client.get(path=url)
        posts = Post.objects.all().annotate(
            username=F('owner__username'),
            post_count=Count('owner__post_owner'),
            user_id=F('owner__id')
        )
        data = PostModelSerializer(posts, many=True).data
        self.assertEqual(first=status.HTTP_200_OK, second=response.status_code)
        self.assertEqual(first=data, second=response.data)

    def test_create_is_authenticated(self):
        """Test for creating post with authenticated user"""

        self.assertEqual(first=1, second=Post.objects.all().count())
        url = reverse('post-list')
        data = {
            'subject': self.subject.id,
            'title': 'new_title',
            'body': 'new_body'
        }
        json_data = json.dumps(data)
        self.client.credentials(HTTP_AUTHORIZATION=self.token)
        response = self.client.post(path=url, content_type='application/json',
                                    data=json_data)
        self.assertEqual(first=status.HTTP_201_CREATED, second=response.status_code)
        self.assertEqual(first=2, second=Post.objects.all().count())

    def test_create_un_authenticated(self):
        """Test for creating post with un authenticated user"""

        url = reverse('post-list')
        data = {
            'subject': self.subject.id,
            'title': 'new_title',
            'body': 'new_body'
        }
        json_data = json.dumps(data)
        response = self.client.post(path=url, content_type='application/json',
                                    data=json_data)
        self.assertEqual(first=status.HTTP_401_UNAUTHORIZED, second=response.status_code)
        self.assertEqual(first=1, second=Post.objects.all().count())

    def test_delete_owner(self):
        """Test for delete post owner"""

        self.assertEqual(first=1, second=Post.objects.all().count())
        url = reverse('post-detail', args=(self.post.id,))
        self.client.credentials(HTTP_AUTHORIZATION=self.token)
        response = self.client.delete(path=url)
        self.assertEqual(first=status.HTTP_204_NO_CONTENT, second=response.status_code)
        self.assertEqual(first=0, second=Post.objects.all().count())

    def test_delete_not_owner(self):
        """Test for delete post not owner"""

        url = reverse('post-detail', args=(self.post.id,))
        response = self.client.delete(path=url)
        self.assertEqual(first=status.HTTP_401_UNAUTHORIZED, second=response.status_code)
        self.assertEqual(first=1, second=Post.objects.all().count())

    def test_update_owner(self):
        """Test for delete post owner"""

        self.assertEqual(first='post', second=self.post.title)
        url = reverse('post-detail', args=(self.post.id,))
        data = {
            'subject': self.subject.id,
            'title': 'new_title',
            'body': 'body'
        }
        json_data = json.dumps(data)
        self.client.credentials(HTTP_AUTHORIZATION=self.token)
        response = self.client.put(path=url, content_type='application/json',
                                   data=json_data)
        self.assertEqual(first=status.HTTP_200_OK, second=response.status_code)
        self.post.refresh_from_db()
        self.assertEqual(first='new_title', second=self.post.title)

    def test_update_not_owner(self):
        """Test for delete post not owner"""

        url = reverse('post-detail', args=(self.post.id,))
        data = {
            'subject': self.subject.id,
            'title': 'new_title',
            'body': 'body'
        }
        json_data = json.dumps(data)
        self.client.credentials(HTTP_AUTHORIZATION=self.token_1)
        response = self.client.put(path=url, content_type='application/json',
                                   data=json_data)
        self.assertEqual(first=status.HTTP_403_FORBIDDEN, second=response.status_code)


class LikeDislikeApiTestCase(APITestCase):
    """Test case for like dislike api view"""

    def setUp(self):
        password = make_password('password')
        url = reverse('token')

        self.user = get_user_model().objects.create(username='user',
                                                    password=password,
                                                    is_active=True,
                                                    is_staff=True)
        data = {
            'username': self.user.username,
            'password': 'password'
        }
        json_data = json.dumps(data)
        self.token = f"Token " \
                     f"{self.client.post(path=url, data=json_data, content_type='application/json').data['access']}"

        self.user_1 = get_user_model().objects.create(username='user_1',
                                                      password=password,
                                                      is_active=True,
                                                      is_staff=True)
        data_1 = {
            'username': self.user_1.username,
            'password': 'password'
        }
        json_data_1 = json.dumps(data_1)
        self.token_1 = f"Token " \
                       f"{self.client.post(path=url, data=json_data_1, content_type='application/json').data['access']}"

        self.subject = Subject.objects.create(subject='subject')
        self.post = Post.objects.create(subject=self.subject, owner=self.user, title='post', body='body')
        self.post_1 = Post.objects.create(subject=self.subject, owner=self.user, title='post_1', body='body_1')
        self.like_dislike = LikeDislike.objects.create(user=self.user, post=self.post, like=1)

    def test_create_like_dislike_authenticated(self):
        """Test Case for creating like of post with authenticated person"""

        self.assertEqual(first=1, second=LikeDislike.objects.all().count())
        url = reverse('post_likes_dislikes', args=(self.post_1.id,))
        data = {
            'like': 1,
            'post': self.post_1.id
        }
        json_data = json.dumps(data)
        self.client.credentials(HTTP_AUTHORIZATION=self.token)
        response = self.client.post(path=url, content_type='application/json',
                                    data=json_data)
        self.assertEqual(first=status.HTTP_201_CREATED, second=response.status_code)
        self.assertEqual(first=2, second=LikeDislike.objects.all().count())

    def test_create_exist_like_dislike_authenticated(self):
        """Test Case for creating exist like of post with authenticated person"""

        self.assertEqual(first=1, second=LikeDislike.objects.all().count())
        url = reverse('post_likes_dislikes', args=(self.post.id,))
        data = {
            'like': 1,
            'post': self.post.id
        }
        json_data = json.dumps(data)
        self.client.credentials(HTTP_AUTHORIZATION=self.token)
        response = self.client.post(path=url, content_type='application/json',
                                    data=json_data)
        self.assertEqual(first=status.HTTP_200_OK, second=response.status_code)
        self.assertEqual(first=1, second=LikeDislike.objects.all().count())

    def test_create_like_dislike_un_authenticated(self):
        """Test Case for creating like of post with un authenticated person"""

        self.assertEqual(first=1, second=LikeDislike.objects.all().count())
        url = reverse('post_likes_dislikes', args=(self.post_1.id,))
        data = {
            'like': 1,
            'post': self.post_1.id
        }
        json_data = json.dumps(data)
        response = self.client.post(path=url, content_type='application/json',
                                    data=json_data)
        self.assertEqual(first=status.HTTP_401_UNAUTHORIZED, second=response.status_code)
        self.assertEqual(first=1, second=LikeDislike.objects.all().count())

    def test_update_like_authenticated(self):
        """Test Case for updating like of post with authenticated person"""

        self.assertEqual(first=1, second=LikeDislike.objects.get(user=self.user, post=self.post).like)
        url = reverse('post_likes_dislikes', args=(self.post.id,))
        data = {
            'like': 1,
            'dislike': 0,
            'post': self.post.id
        }
        json_data = json.dumps(data)
        self.client.credentials(HTTP_AUTHORIZATION=self.token)
        response = self.client.post(path=url, content_type='application/json',
                                    data=json_data)
        self.assertEqual(first=status.HTTP_200_OK, second=response.status_code)
        self.like_dislike.refresh_from_db()
        self.assertEqual(first=1, second=LikeDislike.objects.get(user=self.user, post=self.post).like)
        self.assertEqual(first=0, second=LikeDislike.objects.get(user=self.user, post=self.post).dislike)

    def test_update_dislike_authenticated(self):
        """Test Case for updating dislike of post with authenticated person"""

        self.assertEqual(first=1, second=LikeDislike.objects.get(user=self.user, post=self.post).like)
        url = reverse('post_likes_dislikes', args=(self.post.id,))
        data = {
            'dislike': 1,
            'like': 0,
            'post': self.post.id
        }
        json_data = json.dumps(data)
        self.client.credentials(HTTP_AUTHORIZATION=self.token)
        response = self.client.post(path=url, content_type='application/json',
                                    data=json_data)
        self.assertEqual(first=status.HTTP_200_OK, second=response.status_code)
        self.like_dislike.refresh_from_db()
        self.assertEqual(first=1, second=LikeDislike.objects.get(user=self.user, post=self.post).dislike)
        self.assertEqual(first=0, second=LikeDislike.objects.get(user=self.user, post=self.post).like)


class CommentApiTestCase(APITestCase):
    """Test case for comment api view"""

    def setUp(self):
        password = make_password('password')
        url = reverse('token')

        self.user = get_user_model().objects.create(username='user',
                                                    password=password,
                                                    is_active=True,
                                                    is_staff=True)
        data = {
            'username': self.user.username,
            'password': 'password'
        }
        json_data = json.dumps(data)
        self.token = f"Token " \
                     f"{self.client.post(path=url, data=json_data, content_type='application/json').data['access']}"

        self.user_1 = get_user_model().objects.create(username='user_1',
                                                      password=password,
                                                      is_active=True,
                                                      is_staff=True)
        data_1 = {
            'username': self.user_1.username,
            'password': 'password'
        }
        json_data_1 = json.dumps(data_1)
        self.token_1 = f"Token " \
                       f"{self.client.post(path=url, data=json_data_1, content_type='application/json').data['access']}"

        self.user_2 = get_user_model().objects.create(username='user_2',
                                                      password=password,
                                                      is_active=True)
        data_2 = {
            'username': self.user_2.username,
            'password': 'password'
        }
        json_data_2 = json.dumps(data_2)
        self.token_2 = f"Token " \
                       f"{self.client.post(path=url, data=json_data_2, content_type='application/json').data['access']}"

        self.subject = Subject.objects.create(subject='subject')
        self.post = Post.objects.create(subject=self.subject, owner=self.user, title='post', body='body')
        self.post_1 = Post.objects.create(subject=self.subject, owner=self.user, title='post_1', body='body_1')
        self.comment = Comment.objects.create(user=self.user, post=self.post, text='first_comment')
        self.comment_1 = Comment.objects.create(
            user=self.user,
            post=self.post,
            text='first_comment',
            parent=self.comment)

    def test_get_comments_authenticated(self):
        """Test Case for getting comments with authenticated user"""

        url = reverse('comment-list')
        self.client.credentials(HTTP_AUTHORIZATION=self.token)
        response = self.client.get(path=url)
        self.assertEqual(first=status.HTTP_200_OK, second=response.status_code)

    def test_get_comments_un_authenticated(self):
        """Test Case for getting comments with un authenticated user"""

        url = reverse('comment-list')
        response = self.client.get(path=url)
        self.assertEqual(first=status.HTTP_401_UNAUTHORIZED, second=response.status_code)

    def test_create_comment(self):
        """Test Case for creating comment"""

        self.assertEqual(first=2, second=Comment.objects.all().count())
        url = reverse('comment-list')
        data = {
            'user': self.user.id,
            'post': self.post.id,
            'text': 'first_comment',
            'parent': self.comment.id
        }
        json_data = json.dumps(data)
        self.client.credentials(HTTP_AUTHORIZATION=self.token)
        response = self.client.post(path=url, content_type='application/json',
                                    data=json_data)
        self.assertEqual(first=status.HTTP_201_CREATED, second=response.status_code)
        self.assertEqual(first=3, second=Comment.objects.all().count())

    def test_delete_comment_owner(self):
        """Test Case for deleting main comment owner"""

        self.assertEqual(first=2, second=Comment.objects.all().count())
        url = reverse('comment-detail', args=(self.comment.id,))
        self.client.credentials(HTTP_AUTHORIZATION=self.token)
        response = self.client.delete(path=url)
        self.assertEqual(first=status.HTTP_204_NO_CONTENT, second=response.status_code)
        self.assertEqual(first=0, second=Comment.objects.all().count())

    def test_delete_comment_not_owner(self):
        """Test Case for deleting main comment not owner"""

        url = reverse('comment-detail', args=(self.comment.id,))
        self.client.credentials(HTTP_AUTHORIZATION=self.token_1)
        response = self.client.delete(path=url)
        self.assertEqual(first=status.HTTP_404_NOT_FOUND, second=response.status_code)

    def test_update_comment_owner(self):
        """Test Case for updating main comment not owner"""

        self.assertEqual(first='first_comment', second=Comment.objects.get(id=self.comment.id).text)
        url = reverse('comment-detail', args=(self.comment.id,))
        data = {
            'text': 'new_comment'
        }
        json_data = json.dumps(data)
        self.client.credentials(HTTP_AUTHORIZATION=self.token)
        response = self.client.patch(path=url, content_type='application/json',
                                     data=json_data)
        self.assertEqual(first=status.HTTP_200_OK, second=response.status_code)
        self.comment.refresh_from_db()
        self.assertEqual(first='new_comment', second=Comment.objects.get(id=self.comment.id).text)

    def test_update_comment_not_owner(self):
        """Test Case for updating main comment not owner"""

        self.assertEqual(first='first_comment', second=Comment.objects.get(id=self.comment.id).text)
        url = reverse('comment-detail', args=(self.comment.id,))
        data = {
            'text': 'new_comment'
        }
        json_data = json.dumps(data)
        self.client.credentials(HTTP_AUTHORIZATION=self.token_2)
        response = self.client.patch(path=url, content_type='application/json',
                                     data=json_data)
        self.assertEqual(first=status.HTTP_404_NOT_FOUND, second=response.status_code)
        self.comment.refresh_from_db()
        self.assertEqual(first='first_comment', second=Comment.objects.get(id=self.comment.id).text)
