"""
Views for the user API
"""

from rest_framework import generics, authentication, permissions
from . import serializers
from templateDjangoReact.models import User


class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system"""
    serializer_class = serializers.CreateUserSerializer
    permission_classes = [permissions.AllowAny]

class ManageUserView(generics.RetrieveUpdateDestroyAPIView):
    """Manage the authenticated user."""
    serializer_class = serializers.CreateUserSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = User.objects.all()

class ListUserAPIView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializerFirstLastName
    perimission_classes = [permissions.AllowAny]







