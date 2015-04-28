from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from user_profile.models import UserProfile


@receiver(post_save, sender=User)
def create_profile(sender, **kwargs):
    instance = kwargs.get('instance')
    if kwargs.get('created'):
        up = UserProfile(user=instance)
        up.save()
