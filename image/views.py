from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView
from image.models import Image
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from image.templatetags.image_extras import viewable_public
from operator import attrgetter
from image.disqus import get_disqus_sso
import pprint


class StreamView(ListView):
    model = Image
    template_name = "stream.html"


class UploadImageView(CreateView):
    model = Image
    template_name = "upload_image.html"
    fields = ['picture',
              'title',
              'source',
              'year',
              'description',
              'category',
              'published']

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = form_class(request.POST, request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            image.user = request.user
            image.save()
            return HttpResponseRedirect(
                reverse(
                    'image:library'
                ))
        return self.render_to_response({'form': form})


class EditImageView(UpdateView):
    model = Image
    template_name = "edit_image.html"
    fields = ['picture',
              'title',
              'source',
              'year',
              'description',
              'category',
              'published']

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        instance = Image.objects.get(pk=kwargs['pk'])
        form = form_class(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(
                reverse(
                    'image:library'
                ))
        return self.render_to_response({'form': form})


@login_required
def library_view(request, *args, **kwargs):
    return render(request, 'library.html', {})


@login_required
def gallery_view(request, *args, **kwargs):
    user = User.objects.get(pk=kwargs['pk'])
    context = {'other_user': user}
    return render(request, 'gallery.html', context)


@login_required
def image_page(request, *args, **kwargs):

    image = Image.objects.get(pk=kwargs['pk'])
    images = viewable_public(Image, image.user)
    s_images = sorted(images, key=attrgetter('pk'))

    image_index = s_images.index(image)
    # determine what images are previous and next:
    if image_index > 0:
        prev_image = s_images[image_index - 1].pk
    else:     # set to -1 if already at first image
        prev_image = -1
    if image_index < len(s_images) - 1:
        next_image = s_images[image_index + 1].pk
    else:     # set to -1 if already at last image
        next_image = -1

    #  create image identifier for disqus to use for comments
    identifier = "".join(["image", str(image.pk)])

    #  create disqus sso for user
    user_sso = get_disqus_sso(request.user)

    print user_sso

    context = {'image': image,
               'prev_image': prev_image,
               'next_image': next_image,
               'image_identifier': identifier,
               'user_sso': user_sso}
    return render(request, 'image_page.html', context)
