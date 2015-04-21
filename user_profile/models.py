from django.db import models
from django.contrib.auth.models import User
from django.utils.encoding import python_2_unicode_compatible
from imager.settings import STATIC_URL
import datetime
import os
from django.core.validators import RegexValidator

# Already in User: username, password, date joined, email address, active


class ActiveProfileManager(models.Manager):
    """Profile Manager"""
    def get_queryset(self):
        """gets"""
        query = super(ActiveProfileManager, self).get_queryset()
        return query.filter(is_active__exact=True)


@python_2_unicode_compatible
class UserProfile(models.Model):
    """This sets up a User Profile with privacy settings."""
    PRIVACY_CHOICES = (
        ('PR', 'Private'),
        ('FR', 'Friends'),
        ('PU', 'Public'),
    )

    # new fields
    picture = models.ImageField(default=os.path.join(
        STATIC_URL,
        'images',
        'default_profile_image.jpg'))
    birthday = models.DateField(default=datetime.date.today)
    phone = models.CharField(max_length=15, blank=True, null=True)

    # privacy settings
    pic_privacy = models.CharField(max_length=2, choices=PRIVACY_CHOICES,
                                   default='PR')
    birthday_privacy = models.CharField(max_length=2, choices=PRIVACY_CHOICES,
                                        default='PR')
    phone_privacy = models.CharField(max_length=2, choices=PRIVACY_CHOICES,
                                     default='PR')
    name_privacy = models.CharField(max_length=2, choices=PRIVACY_CHOICES,
                                    default='PR')
    email_privacy = models.CharField(max_length=2, choices=PRIVACY_CHOICES,
                                     default='PR')

    # Associates profile to the User model
    user = models.OneToOneField(User, related_name='profile')
    is_active = models.BooleanField(default=True)

    following = models.ManyToManyField('self',
                                       null=True,
                                       symmetrical=False,
                                       related_name='followers')

    blocking = models.ManyToManyField('self',
                                      null=True,
                                      symmetrical=False,
                                      related_name='blockers')
    objects = models.Manager()
    active = ActiveProfileManager()

    def __str__(self):
        return self.user.username

    # Following
    def follow(self, other):
        self.following.add(other)

    def unfollow(self, other):
        if other in self.following.all():
            self.following.remove(other)
        else:
            raise ValueError('Cannot unfollow someone you are not following.')

    # def following(self):
    #     return self.follows.exclude(blocking=self)

    # Blocking
    def block(self, other):
        return self.blocking.add(other)

    def unblock(self, other):
        if other in self.following.all():
            self.blocking.remove(other)
        else:
            raise ValueError('Cannot unblock someone you are not blocking.')
