"""
Serializer for User API
"""

from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers
from templateDjangoReact.models import User
from django.utils.translation import gettext_lazy as _


class CreateUserSerializer(serializers.ModelSerializer):
    """Serializer for the user object."""

    class Meta:
        model = get_user_model()
        fields = ['id', 'email', 'password',
                  'first_name', 'last_name', 'date_joined',]
        extra_kwargs = {'password': {'write_only': True, 'min_length': 7}}

    def create(self, validated_data):
        """Create and return user with encrypted data"""
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """Update API user data"""
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user


class UserSerializerFirstLastName(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email']
