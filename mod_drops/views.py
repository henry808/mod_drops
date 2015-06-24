from django.shortcuts import render
from image.models import Image


def index(request):
    try:
        random_image = Image.objects.filter(
            published='pub').order_by('?')[0].image.url
    except IndexError:
        random_image = "test"
    context = {'random_image': random_image,
               'request': request}
    return render(request, 'index.html', context)


def about(request):

    context = {'request': request}
    return render(request, 'about.html', context)
