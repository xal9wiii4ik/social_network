from django.contrib.auth import get_user_model

from rest_framework import serializers


def verification_unique_email(email: str) -> str:
    """Check unique email"""

    user_model = get_user_model()
    try:
        user_model.objects.get(email=email)
    except Exception:
        return email
    else:
        raise serializers.ValidationError('User with given credentials already exist')


def verification_password(value: str) -> str:
    """check password"""

    if len(value) >= 8:
        if any((c in set('QAZWSXEDCRFVTGBYHNUJMIKOLP')) for c in value):
            if any((f in set('1234567890') for f in value)):
                return value
            else:
                raise serializers.ValidationError('Password must contain at least 1 number')
        else:
            raise serializers.ValidationError('Password must contain at least 1 uppercase letter')
    else:
        raise serializers.ValidationError('Password must have to have at least 8 characters')
