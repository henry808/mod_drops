from django.shortcuts import render
from image.models import Image


def index(request):
    random_images = []
    image_count = 4
    while image_count > 0:
        # does not work if less than 4 images in database
        try:
            random_images.append(Image.objects.order_by('?')[0])
            # random_image = Image.objects.filter(
            #     published='pub').order_by('?')[0].image.url
        except IndexError:
            random_images.append("test")
        image_count -= 1
    print random_images
    context = {'random_images': random_images,
               'request': request}
    return render(request, 'index.html', context)


def about(request):

    context = {'request': request}
    return render(request, 'about.html', context)
