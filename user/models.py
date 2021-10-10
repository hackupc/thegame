from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models


class User(AbstractBaseUser):
    USR_ORGANIZER = 'O'
    USR_VOLUNTEER = 'V'
    USR_HACKER = 'H'
    USR_MENTOR = 'M'
    USR_SPONSOR = 'S'
    USR_HACKER_NAME = 'Hacker'
    USR_MENTOR_NAME = 'Mentor'
    USR_SPONSOR_NAME = 'Sponsor'
    USR_VOLUNTEER_NAME = 'Volunteer'
    USR_ORGANIZER_NAME = 'Organizer'

    USR_TYPE = [
        (USR_HACKER, USR_HACKER_NAME),
        (USR_MENTOR, USR_MENTOR_NAME),
        (USR_SPONSOR, USR_SPONSOR_NAME),
        (USR_VOLUNTEER, USR_VOLUNTEER_NAME),
        (USR_ORGANIZER, USR_ORGANIZER_NAME),
    ]

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['name', ]

    email = models.EmailField(
        verbose_name='email',
        max_length=255,
        unique=True,
    )
    name = models.CharField(
        verbose_name='Full name',
        max_length=255,
    )
    type = models.CharField(choices=USR_TYPE, default=USR_HACKER, max_length=2)
    is_admin = models.BooleanField(default=False)

    def has_perm(self, perm, obj=None):
        """Does the user have a specific permission?"""
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        """Does the user have permissions to view the app `app_label`?"""
        # Simplest possible answer: Yes, always
        return True

    def get_full_name(self):
        # The user is identified by their nickname/full_name address
        return self.name

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):
        return self.email

    @property
    def is_superuser(self):
        return self.is_organizer

    @property
    def is_staff(self):
        """Is the user a member of staff?"""
        return self.is_organizer

    @property
    def is_organizer(self):
        return self.type == self.USR_ORGANIZER
