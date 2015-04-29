
from django.db import models
from django.contrib.auth.models import User
from django.utils.encoding import python_2_unicode_compatible
import datetime


# Create your models here.
@python_2_unicode_compatible
class Image(models.Model):
    user = models.ForeignKey(User, related_name='images')
    picture = models.ImageField()
    date_uploaded = models.DateField(auto_now_add=True)
    date_modified = models.DateField(auto_now=True)
    # TODO: change date_published to only write when an image is shared
    date_published = models.DateField(blank=True, null=True)

    title = models.CharField(max_length=(63), blank=True)
    source = models.CharField(max_length=(127), blank=True)

    YEAR_CHOICES = []
    for r in range(1955, datetime.datetime.now().year+1):
        YEAR_CHOICES.append((r, r))

    year = models.IntegerField(max_length=4, choices=YEAR_CHOICES,
                               default=1960,
                               error_messages='not valid year',
                               help_text='please enter a year between 1955 and present')

    description = models.TextField(max_length=(255), blank=True)

    IMAGE = 'IM'    # photos, drawings, and other images
    MUSIC = 'MU'    # album covers, band photos and other images
    MOVIE = 'MO'    # stills, screen captures from movies, or movie posters
    FASHION = 'FA'  # pictures and images of clothes, accessories, etc.
    ICON = 'IC'     # pictures, or drawings of actors or actresses

    PRIVACY_CHOICES = (
        (IMAGE, 'Private'),
        (MUSIC, 'Shared'),
        (MOVIE, 'Public'),
        (FASHION, 'Fashion'),
        (ICON, 'Icon'),
    )

    category = models.CharField(max_length=2, choices=PRIVACY_CHOICES,
                                default=IMAGE)

    PRIVATE = 'PR'
    SHARED = 'SH'
    PUBLIC = 'PU'

    PRIVACY_CHOICES = (
        (PRIVATE, 'Private'),
        (SHARED, 'Shared'),
        (PUBLIC, 'Public'),
    )

    published = models.CharField(max_length=2, choices=PRIVACY_CHOICES,
                                 default=PRIVATE)

    def __str__(self):
        if self.title:
            return self.title
        else:
            return str(self.picture)

    class Meta:
        ordering = ['-date_uploaded']


def get_image():
    """Returns a random public image"""
    try:
        return Image.objects.filter(published=Image.PUBLIC).order_by('?')[0].pk
    except IndexError:
        pass
