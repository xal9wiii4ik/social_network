from django.contrib.auth import get_user_model

from rest_framework import serializers


class AbstractUserOwnerModelSerializer(serializers.ModelSerializer):
    """Model Serializer for abstract user(owner)"""

    class Meta:
        model = get_user_model()
        exclude = ('date_joined',)


class AbstractUserGuestsModelSerializer(serializers.ModelSerializer):
    """Model Serializer for abstract user(guest)"""

    follower_id = serializers.SerializerMethodField

    def get_follower_id(self, obj):
        return 1

    class Meta:
        model = get_user_model()
        fields = ['id', 'first_name', 'last_name', 'phone', 'gender', 'avatar', 'username']
