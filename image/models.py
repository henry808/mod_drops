
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

    UNKNOWN = 'unknown'   # if year is unknown

    YEAR_CHOICES = [('unknown', 'unknown')]
    for r in range(1955, datetime.datetime.now().year+1):

        YEAR_CHOICES.append((str(r), str(r)))

    help_text1 = 'please enter a year between 1955 and present'

    year = models.CharField(max_length=7, choices=YEAR_CHOICES,
                               default=UNKNOWN,
                               help_text=help_text1)

    description = models.TextField(max_length=(255), blank=True)

    IMAGE = 'IM'    # photos, drawings, and other images
    MUSIC = 'MU'    # album covers, band photos and other images
    MOVIE = 'MO'    # stills, screen captures from movies, or movie posters
    FASHION = 'FA'  # pictures and images of clothes, accessories, etc.
    ICON = 'IC'     # pictures, or drawings of actors or actresses

    PRIVACY_CHOICES = (
        (IMAGE, 'Image'),
        (MUSIC, 'Music'),
        (MOVIE, 'Movie'),
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
