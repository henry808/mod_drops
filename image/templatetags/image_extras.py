from django import template
from image.models import Image
from django.db.models import Q


register = template.Library()

# Custom filter, return images that are public, shared, or belong to a logged in user
@register.filter
def viewable(self, user):
    return Image.objects.filter(
        Q(user=user) |
        Q(published=Image.SHARED) |
        Q(published=Image.PUBLIC)
        )

# Return images belonging only to one user.
@register.filter
def viewable_user(self, user):
    return Image.objects.filter(Q(user=user))
