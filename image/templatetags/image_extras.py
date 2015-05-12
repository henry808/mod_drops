from django import template
from image.models import Image
from django.db.models import Q

register = template.Library()


# Custom filter, return all images that are:
#    public, shared, or belong to a logged in user
@register.filter
def viewable(self, user):
    query = Image.objects.filter(
        Q(user=user) |
        Q(published=Image.SHARED) |
        Q(published=Image.PUBLIC)
        )
    orders = ['pk']
    result = query.order_by(*orders)
    if len(result) > 0:
        return result
    else:
        return []


# Return all images belonging only to one user.
@register.filter
def viewable_user(self, user):
    query = Image.objects.filter(Q(user=user))
    orders = ['pk']
    result = query.order_by(*orders)
    if len(result) > 0:
        return result
    else:
        return []

# Return public images belonging only to one user.
@register.filter
def viewable_other_user(self, user):
    query = Image.objects.filter(Q(user=user) &
            Q(published=Image.PUBLIC))
    orders = ['pk']
    result = query.order_by(*orders)
    if len(result) > 0:
        return result
    else:
        return []
