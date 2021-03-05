from rest_framework import serializers

from apps.auth_user.services_serializers import (
    verification_unique_email,
    verification_password,
)


class RegistrationSerializer(serializers.Serializer):
    """Сериализатор для регистрации пользователя"""

    first_name = serializers.CharField(max_length=25, required=True)
    last_name = serializers.CharField(max_length=25, required=True)
    email = serializers.EmailField(max_length=60, required=True)
    username = serializers.CharField(max_length=60, required=True)
    password = serializers.CharField(max_length=60, required=True)
    repeat_password = serializers.CharField(max_length=60, required=True)

    def validate_email(self, value: str) -> str:
        """Валидация почты"""

        return verification_unique_email(email=value)

    def validate_password(self, value: str) -> str:
        """Password validation"""

        return verification_password(value=value)


class LogInSerializer(serializers.Serializer):
    """Serializer for log in"""

    username = serializers.CharField(max_length=150, required=True)
    password = serializers.CharField(max_length=128, required=True)


class ResetPasswordSerializer(serializers.Serializer):
    """Serializer for reset password before set password"""

    email = serializers.EmailField(required=True)


class SetPasswordSerializer(serializers.Serializer):
    """Serializer for set password after the confirmation"""

    password = serializers.CharField(max_length=128, required=True)
    repeat_password = serializers.CharField(max_length=128, required=True)

    def validate_password(self, value: str) -> str:
        """Password validation"""

        return verification_password(value=value)
