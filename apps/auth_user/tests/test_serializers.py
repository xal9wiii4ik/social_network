from django.contrib.auth import get_user_model
from django.test import TestCase

from apps.auth_user.serializers import (
    RegistrationSerializer,
    LogInSerializer,
    ResetPasswordSerializer,
    SetPasswordSerializer,
)


class RegistrationSerializerTestCase(TestCase):
    """Test for RegistrationSerializer"""

    def test_valid_data(self):
        """valid data"""

        data = {
            'first_name': 'first_name',
            'last_name': 'last_name',
            'email': 'email@mail.ru',
            'username': 'username',
            'password': 'Password1',
            'repeat_password': 'Password1',
        }
        self.assertTrue(RegistrationSerializer(data=data).is_valid())

    def test_un_valid_mail(self):
        """un valid mail"""

        data = {
            'first_name': 'first_name',
            'last_name': 'last_name',
            'email': 'emailmail.ru',
            'username': 'username',
            'password': 'Password1',
            'repeat_password': 'Password1',
        }
        self.assertFalse(RegistrationSerializer(data=data).is_valid())

    def test_un_valid_password_less_then_8_characters(self):
        """un valid password"""

        data = {
            'first_name': 'first_name',
            'last_name': 'last_name',
            'email': 'email@mail.ru',
            'username': 'username',
            'password': 'pass',
            'repeat_password': 'pass',
        }
        self.assertFalse(RegistrationSerializer(data=data).is_valid())

    def test_un_valid_password_with_out_capital_letter(self):
        """un valid password"""

        data = {
            'first_name': 'first_name',
            'last_name': 'last_name',
            'email': 'email@mail.ru',
            'username': 'username',
            'password': '12345678',
            'repeat_password': '12345678',
        }
        self.assertFalse(RegistrationSerializer(data=data).is_valid())

    def test_un_valid_password_with_out_numbers(self):
        """un valid password"""

        data = {
            'first_name': 'first_name',
            'last_name': 'last_name',
            'email': 'email@mail.ru',
            'username': 'username',
            'password': 'asdAASDa',
            'repeat_password': 'asdAASDa',
        }
        self.assertFalse(RegistrationSerializer(data=data).is_valid())


class LoginSerializerTestCase(TestCase):
    """Test for LoginSerializer"""

    def setUp(self):
        get_user_model().objects.create(username='username', email='username@mail.ru')

    def test_valid_data(self):
        """valid data"""

        data = {
            'username': 'username@mail.ru',
            'password': 'password'
        }
        serializer = LogInSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual('username@mail.ru', serializer.data['username'])

    def test_un_valid_data_mail(self):
        """un valid data"""

        data = {
            'email': 'userna@mail.ru',
            'password': 'password'
        }
        serializer = LogInSerializer(data=data)
        self.assertFalse(serializer.is_valid())


class ResetPasswordSerializerTestCase(TestCase):
    """Test for ResetPassword"""

    def setUp(self):
        get_user_model().objects.create(username='username', email='username@mail.ru')

    def test_valid_data(self):
        """valid data"""

        data = {
            'email': 'username@mail.ru'
        }
        self.assertTrue(ResetPasswordSerializer(data=data).is_valid())

    def test_un_valid_data_mail(self):
        """valid data"""

        data = {
            'username': 'usern@mail.ru'
        }
        self.assertFalse(ResetPasswordSerializer(data=data).is_valid())


class SetPasswordSerializerTestCase(TestCase):
    """Test for SetPassword"""

    def test_valid_data(self):
        """valid data"""

        data = {
            'password': 'Password1',
            'repeat_password': 'Password1'
        }
        self.assertTrue(SetPasswordSerializer(data=data).is_valid())

    def test_un_valid_password_less_then_8_characters(self):
        """un valid password"""

        data = {
            'password': 'pass',
            'repeat_password': 'pass',
        }
        self.assertFalse(SetPasswordSerializer(data=data).is_valid())

    def test_un_valid_password_with_out_capital_letter(self):
        """un valid password"""

        data = {
            'password': '12345678',
            'repeat_password': '12345678',
        }
        self.assertFalse(SetPasswordSerializer(data=data).is_valid())

    def test_un_valid_password_with_out_numbers(self):
        """un valid password"""

        data = {
            'password': 'asdAASDa',
            'repeat_password': 'asdAASDa',
        }
        self.assertFalse(SetPasswordSerializer(data=data).is_valid())
