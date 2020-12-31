from django.contrib.auth import get_user_model

from rest_framework import serializers


class AbstractUserOwnerModelSerializer(serializers.ModelSerializer):
    """Model Serializer for abstract user"""

    class Meta:
        model = get_user_model()
        fields = '__all__'


class AbstractUserGuestsModelSerializer(serializers.ModelSerializer):
    """Model Serializer for abstract user"""

    class Meta:
        model = get_user_model()
        fields = ['id', 'first_name', 'last_name', 'phone', 'gender', 'avatar']
