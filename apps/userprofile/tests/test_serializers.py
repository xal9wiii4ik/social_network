from django.contrib.auth import get_user_model
from django.db.models import F
from django.test import TestCase

from apps.userprofile.serializers import (
    AbstractUserGuestsModelSerializer,
    AbstractUserOwnerModelSerializer,
)


class AbstractUserGuestsModelSerializerTestCase(TestCase):
    """Test case for Abstract User Guests Model Serializer"""

    def test_ok(self):
        user = get_user_model().objects.create(
            username='user',
            first_name='Nikita',
            last_name='Zaretskiy',
            phone='+375292125976',
            gender='male'
        )
        user_1 = get_user_model().objects.create(
            username='user_1',
            first_name='Natasha',
            last_name='Zaretskiy',
            phone='+3753330470008',
            gender='female',
        )

        users = get_user_model().objects.all()
        data = AbstractUserGuestsModelSerializer(users, many=True).data
        expected_data = [
            {
                'id': user.id,
                'first_name': 'Nikita',
                'last_name': 'Zaretskiy',
                'phone': '+375292125976',
                'gender': 'male',
                'avatar': None,
                'username': 'user'
            },
            {
                'id': user_1.id,
                'first_name': 'Natasha',
                'last_name': 'Zaretskiy',
                'phone': '+3753330470008',
                'gender': 'female',
                'avatar': None,
                'username': 'user_1'
            }
        ]
        self.assertEqual(first=expected_data, second=data)


class AbstractUserOwnerModelSerializerTestCase(TestCase):
    """Test case for Abstract User Owner Model Serializer"""

    def test_ok(self):
        user = get_user_model().objects.create(
            username='user',
            first_name='Nikita',
            last_name='Zaretskiy',
            phone='+375292125976',
            gender='male',
            email='xal9wa@gmail.com',
            is_superuser=True
        )
        user_1 = get_user_model().objects.create(
            username='user_1',
            first_name='Natasha',
            last_name='Zaretskiy',
            phone='+3753330470008',
            gender='female'
        )
        users = get_user_model().objects.all()
        data = AbstractUserOwnerModelSerializer(users, many=True).data
        expected_data = [
            {
                'id': user.id,
                'password': '',
                'last_login': None,
                'is_superuser': True,
                'username': 'user',
                'first_name': 'Nikita',
                'last_name': 'Zaretskiy',
                'email': 'xal9wa@gmail.com',
                'is_staff': False,
                'is_active': True,
                'gender': 'male',
                'phone': '+375292125976',
                'avatar': None,
                'followers': 0,
                'subscribers': 0,
                'groups': [],
                'user_permissions': []
            },
            {
                'id': user_1.id,
                'password': '',
                'last_login': None,
                'is_superuser': False,
                'username': 'user_1',
                'first_name': 'Natasha',
                'last_name': 'Zaretskiy',
                'email': '',
                'is_staff': False,
                'is_active': True,
                'gender': 'female',
                'phone': '+3753330470008',
                'avatar': None,
                'followers': 0,
                'subscribers': 0,
                'groups': [],
                'user_permissions': []
            }
        ]
        self.assertEqual(first=expected_data, second=data)
