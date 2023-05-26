from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db.models.signals import pre_save, post_save
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
import datetime
from decimal import Decimal
from .managers import CustomUserManager


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    first_name = models.CharField(
        _('first name'), max_length=150, blank=True, null=True)
    last_name = models.CharField(
        _('last name'), max_length=150, blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()
    class Meta:
        get_latest_by = ['last_update']

    def __str__(self):
        return self.email
