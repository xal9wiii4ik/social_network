from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.exceptions import ValidationError

from apps.auth_user.services_serializers import (
    verification_password,
    verification_unique_email,
)


class ServicesSerializerTestCase(TestCase):
    """Test for services"""

    def setUp(self):
        self.user = get_user_model().objects.create(username='user',
                                                    email='email@mail.ru')

    def test_verification_password_un_valid_least_8(self):
        """un valid password"""

        try:
            verification_password(value='1234567')
        except ValidationError:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

    def test_verification_password_un_valid_only_numbers(self):
        """un valid password"""

        try:
            verification_password(value='12345678')
        except ValidationError:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

    def test_verification_password_un_valid_no_contain_upper_latter(self):
        """un valid password"""

        try:
            verification_password(value='12345678')
        except ValidationError:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

    def test_verification_password_un_valid_no_contain_number(self):
        """un valid password"""

        try:
            verification_password(value='aaaaaaaAAAAA')
        except ValidationError:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

    def test_verification_password_valid(self):
        """un valid password"""

        self.assertEqual('aaaaaaaAAAAA1', verification_password('aaaaaaaAAAAA1'))

    def test_verification_unique_email(self):
        """verification unique email"""

        self.assertEqual('exist@mail.ru',
                         verification_unique_email('exist@mail.ru'))
