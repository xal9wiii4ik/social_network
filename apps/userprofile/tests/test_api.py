import json

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from rest_framework import status

from rest_framework.reverse import reverse
from rest_framework.test import APITestCase


class AbstractUserOwnerApiViewTest(APITestCase):
    """Api test for Abstract User Owner View Set"""

    def setUp(self):
        password = make_password('password')
        url = reverse('token')

        self.user = get_user_model().objects.create(
            username='user',
            first_name='Nikita',
            last_name='Zaretskiy',
            phone='+375292125976',
            gender='male',
            email='xal9wa@gmail.com',
            is_superuser=True,
            password=password
        )
        data = {
            'username': self.user.username,
            'password': 'password'
        }
        json_data = json.dumps(data)
        self.token = f"Token " \
                     f"{self.client.post(path=url, data=json_data, content_type='application/json').data['access']}"

        self.user_1 = get_user_model().objects.create(
            username='user_1',
            first_name='Natasha',
            last_name='Zaretskiy',
            phone='+3753330470008',
            gender='female',
            password=password
        )
        data_1 = {
            'username': self.user_1.username,
            'password': 'password'
        }
        json_data_1 = json.dumps(data_1)
        self.token_1 = f"Token " \
                       f"{self.client.post(path=url, data=json_data_1, content_type='application/json').data['access']}"

    def test_get_user_owner(self):
        """Test for getting user profile with owner"""

        url = reverse('customuser-detail', args=(self.user.id,))
        self.client.credentials(HTTP_AUTHORIZATION=self.token)
        response = self.client.get(path=url)
        self.assertEqual(first=status.HTTP_200_OK, second=response.status_code)

    def test_get_user_not_owner(self):
        """Test for getting user profile with not owner"""

        url = reverse('customuser-detail', args=(self.user.id,))
        self.client.credentials(HTTP_AUTHORIZATION=self.token_1)
        response = self.client.get(path=url)
        self.assertEqual(first=status.HTTP_403_FORBIDDEN, second=response.status_code)

    def test_get_user_not_owner_un_authenticated(self):
        """Test for getting user profile with not owner un authenticated"""

        url = reverse('customuser-detail', args=(self.user.id,))
        response = self.client.get(path=url)
        self.assertEqual(first=status.HTTP_401_UNAUTHORIZED, second=response.status_code)

    def test_delete_user_owner(self):
        """Test for deleting user profile with owner"""

        self.assertEqual(first=2, second=get_user_model().objects.all().count())
        url = reverse('customuser-detail', args=(self.user.id,))
        self.client.credentials(HTTP_AUTHORIZATION=self.token)
        response = self.client.delete(path=url)
        self.assertEqual(first=status.HTTP_204_NO_CONTENT, second=response.status_code)
        self.assertEqual(first=1, second=get_user_model().objects.all().count())

    def test_delete_user_not_owner(self):
        """Test for deleting user profile with not owner"""

        self.assertEqual(first=2, second=get_user_model().objects.all().count())
        url = reverse('customuser-detail', args=(self.user.id,))
        self.client.credentials(HTTP_AUTHORIZATION=self.token_1)
        response = self.client.delete(path=url)
        self.assertEqual(first=status.HTTP_403_FORBIDDEN, second=response.status_code)
        self.assertEqual(first=2, second=get_user_model().objects.all().count())

    def test_update_user_owner(self):
        """Test for updating user profile with owner"""

        self.assertEqual(first='user', second=self.user.username)
        url = reverse('customuser-detail', args=(self.user.id,))
        data = {
            'username': 'new_username'
        }
        json_data = json.dumps(data)
        self.client.credentials(HTTP_AUTHORIZATION=self.token)
        response = self.client.patch(path=url, content_type='application/json',
                                     data=json_data)
        self.assertEqual(first=status.HTTP_200_OK, second=response.status_code)
        self.user.refresh_from_db()
        self.assertEqual(first='new_username', second=self.user.username)

    def test_update_user_not_owner(self):
        """Test for updating user profile with not owner"""

        self.assertEqual(first='user', second=self.user.username)
        url = reverse('customuser-detail', args=(self.user.id,))
        data = {
            'username': 'new_username'
        }
        json_data = json.dumps(data)
        self.client.credentials(HTTP_AUTHORIZATION=self.token_1)
        response = self.client.patch(path=url, content_type='application/json',
                                     data=json_data)
        self.assertEqual(first=status.HTTP_403_FORBIDDEN, second=response.status_code)
        self.user.refresh_from_db()
        self.assertEqual(first='user', second=self.user.username)
