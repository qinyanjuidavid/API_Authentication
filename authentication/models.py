# from typing_extensions import Required
from django.contrib.auth import validators
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.db.models.fields import EmailField
from django.utils.translation import gettext as _
from todos.helpers.models import TrackingModel


class CustomManager(BaseUserManager):
    def create_user(self, email, username, password=None,
                    is_active=True, is_admin=False,
                    is_staff=False):
        if not email:
            raise ValueError("Users must have an email!")
        if not password:
            raise ValueError("Users must have a password!")
        if not username:
            raise ValueError("Users must have  a username!")
        user_obj = self.model(
            email=self.normalize_email(email), username=username
        )
        user_obj.set_password(password)
        user_obj.is_active = is_active
        user_obj.is_admin = is_admin
        user_obj.is_staff = is_staff
        user_obj.save(using=self._db)

        return user_obj

    def create_staff(self, email, username, password=None):
        user = self.create_user(
            email, username,
            password=password, is_active=True,
            is_staff=True, is_admin=False,
        )
        return user

    def create_superuser(self, email, username, password=None):
        user = self.create_user(
            email, username,
            password=password, is_active=True,
            is_staff=True, is_admin=True,
        )
        return user


class User(AbstractBaseUser, TrackingModel):
    username_validator = UnicodeUsernameValidator()
    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        validators=[username_validator],
        error_messages={
            'unique': ('A user with that username already exists.')
        },
    )

    first_name = models.CharField(_('First name'), max_length=150)
    email = models.EmailField(
        _('Email Address'),
        unique=True,
        error_messages={
            'unique': ('A user with that email already exists.')
        }
    )
    is_staff = models.BooleanField(
        _("Staff status"),
        default=False,
        help_text=_(
            'Designates whether the user can log into this admin panel')
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
    )
    is_admin = models.BooleanField(
        _("admin"),
        default=False,
    )
    date_joined = models.DateTimeField(
        _('date_joined'),
        auto_now_add=True
    )
    email_verified = models.BooleanField(
        _("Verified"),
        default=False
    )

    objects = CustomManager()
    # EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', ]

    def __str__(self):
        return str(self.username)

    @property
    def token(self):
        return ''

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def staff(self):
        return self.staff

    @property
    def active(self):
        return self.active

    @property
    def admin(self):
        return self.admin
