import json

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.db.models import F

from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from apps.followers.models import Follower
from apps.followers.serializers import FollowerModelSerializer


class FollowerApiTestCase(APITestCase):
    """Api test case for model follower"""

    def setUp(self):
        password = make_password('password')
        url = reverse('token')

        self.user = get_user_model().objects.create(username='user',
                                                    password=password,
                                                    is_active=True)
        data = {
            'username': self.user.username,
            'password': 'password'
        }
        json_data = json.dumps(data)
        self.token = f"Token " \
                     f"{self.client.post(path=url, data=json_data, content_type='application/json').data['access']}"

        self.user_1 = get_user_model().objects.create(username='user_1',
                                                      password=password,
                                                      is_active=True)
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
        self.follower_user = Follower.objects.create(owner=self.user, follower=self.user_1)

    def test_get_followers_authenticated(self):
        """Test api for getting with authentication user list of followers"""

        url = reverse('follower-list')
        self.client.credentials(HTTP_AUTHORIZATION=self.token)
        response = self.client.get(path=url)
        followers = Follower.objects.filter(owner=self.user).annotate(follower_name=F('follower__username'))
        self.assertEqual(first=status.HTTP_200_OK, second=response.status_code)
        self.assertEqual(first=FollowerModelSerializer(followers, many=True).data,
                         second=response.data)

    def test_get_followers_un_authenticated(self):
        """Test api for getting with un authentication user list of followers"""

        url = reverse('follower-list')
        response = self.client.get(path=url)
        self.assertEqual(first=status.HTTP_401_UNAUTHORIZED, second=response.status_code)

    def test_create_un_exist_follower_authenticated(self):
        """Test api for create un exist follower with authentication user"""

        self.assertEqual(1, Follower.objects.all().count())
        url = reverse('follower-list')
        data = {
            'owner': self.user.id,
            'follower': self.user_2.id
        }
        json_data = json.dumps(data)
        self.client.credentials(HTTP_AUTHORIZATION=self.token)
        response = self.client.post(path=url, content_type='application/json',
                                    data=json_data)
        self.assertEqual(first=status.HTTP_201_CREATED, second=response.status_code)
        self.user.refresh_from_db()
        self.user_2.refresh_from_db()
        self.assertEqual(first=2, second=self.user.followers)
        self.assertEqual(first=1, second=self.user_2.subscribers)
        self.assertEqual(first=2, second=Follower.objects.all().count())

    def test_create_exist_follower_authenticated(self):
        """Test api for create exist follower with authentication user"""

        self.assertEqual(1, Follower.objects.all().count())
        url = reverse('follower-list')
        data = {
            'owner': self.user.id,
            'follower': self.user_1.id
        }
        json_data = json.dumps(data)
        self.client.credentials(HTTP_AUTHORIZATION=self.token)
        response = self.client.post(path=url, content_type='application/json',
                                    data=json_data)
        self.assertEqual(first=status.HTTP_400_BAD_REQUEST, second=response.status_code)
        self.assertEqual(first=1, second=Follower.objects.all().count())

    def test_create_follower_un_authenticated(self):
        """Test api for create follower with un authentication user"""

        url = reverse('follower-list')
        data = {
            'owner': self.user.id,
            'follower': self.user_1.id
        }
        json_data = json.dumps(data)
        response = self.client.post(path=url, content_type='application/json',
                                    data=json_data)
        self.assertEqual(first=status.HTTP_401_UNAUTHORIZED, second=response.status_code)

    def test_delete_subscribe_owner(self):
        """Test api for delete subscribe with owner"""

        self.assertEqual(first=1, second=Follower.objects.all().count())
        url = reverse('follower-detail', args=(self.user_1.id,))

        self.client.credentials(HTTP_AUTHORIZATION=self.token)
        response = self.client.delete(path=url)

        self.assertEqual(first=status.HTTP_204_NO_CONTENT, second=response.status_code)
        self.assertEqual(first=0, second=Follower.objects.all().count())
        self.user.refresh_from_db()
        self.user_2.refresh_from_db()
        self.assertEqual(first=0, second=self.user.followers)
        self.assertEqual(first=0, second=self.user_2.subscribers)

    def test_delete_subscribe_not_owner(self):
        """Test api for delete subscribe with not owner"""

        self.assertEqual(first=1, second=Follower.objects.all().count())
        url = reverse('follower-detail', args=(self.user_1.id,))

        self.client.credentials(HTTP_AUTHORIZATION=self.token_1)
        response = self.client.delete(path=url)

        self.assertEqual(first=status.HTTP_400_BAD_REQUEST, second=response.status_code)
        self.assertEqual(first=1, second=Follower.objects.all().count())
