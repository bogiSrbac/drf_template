"""
URLS for User api
"""

from django.urls import path
from . import views

app_name = 'user'

urlpatterns = [
    path('signup/', views.CreateUserView.as_view(), name='signup'),
    path('user/<int:pk>/', views.ManageUserView.as_view(), name='update-user'),
    path('users/', views.ListUserAPIView.as_view(), name='users'),
]

