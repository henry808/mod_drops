from django import template
from image.models import Image
from django.db.models import Q

register = template.Library()


# Custom filter, return images that are:
#     public, shared, or belong to a logged in user
@register.filter
def viewable(self, user):
    query = Image.objects.filter(
        Q(user=user) |
        Q(published=Image.SHARED) |
        Q(published=Image.PUBLIC)
        )
    if len(query) > 0:
        return query
    else:
        return []


# Return images belonging only to one user.
@register.filter
def viewable_user(self, user):
    query = Image.objects.filter(Q(user=user))
    if len(query) > 0:
        return query
    else:
        return []
