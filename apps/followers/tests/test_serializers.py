from django.contrib.auth import get_user_model
from django.db.models import F
from django.test import TestCase

from apps.followers.models import Follower
from apps.followers.serializers import FollowerModelSerializer


class FollowerModelSerializerTestCase(TestCase):
    """Test case for Follower Model Serializer"""

    def test_ok(self):
        self.user = get_user_model().objects.create(username='user',
                                                    is_active=True)
        self.user_1 = get_user_model().objects.create(username='user_1',
                                                      is_active=True)
        self.follower_user = Follower.objects.create(owner=self.user, follower=self.user_1)

        followers = Follower.objects.all().annotate(follower_name=F('owner__username'))
        data = FollowerModelSerializer(followers, many=True).data
        expected_data = [
            {
                'owner': self.user.id,
                'follower': self.user_1.id,
                'follower_name': 'user'
            }
        ]
        self.assertEqual(first=expected_data, second=data)
