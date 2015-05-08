from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView
from image.models import Image
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from image.templatetags.image_extras import viewable_other_user
from operator import attrgetter

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
    images = viewable_other_user(Image, image.user)
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
    context = {'image': image,
               'prev_image': prev_image,
               'next_image': next_image}
    return render(request, 'image_page.html', context)

from django.contrib.auth import REDIRECT_FIELD_NAME
from django.shortcuts import resolve_url
from django.utils.http import is_safe_url
from django.contrib.sites.shortcuts import get_current_site
from django.template.response import TemplateResponse
from django.utils.translation import ugettext as _

@login_required
def exit_image_page(request, next_page=None,
           template_name='registration/logged_out.html',
           redirect_field_name=REDIRECT_FIELD_NAME,
           current_app=None, extra_context=None):
    """
    Logs out the user and displays 'You are logged out' message.
    """

    if next_page is not None:
        next_page = resolve_url(next_page)

    if (redirect_field_name in request.POST or
            redirect_field_name in request.GET):
        next_page = request.POST.get(redirect_field_name,
                                     request.GET.get(redirect_field_name))
        # Security check -- don't allow redirection to a different host.
        if not is_safe_url(url=next_page, host=request.get_host()):
            next_page = request.path

    if next_page:
        # Redirect to this page until the session has been cleared.
        return HttpResponseRedirect(next_page)

    current_site = get_current_site(request)
    context = {
        'site': current_site,
        'site_name': current_site.name,
        'title': _('Logged out')
    }
    if extra_context is not None:
        context.update(extra_context)
    return TemplateResponse(request, template_name, context,
        current_app=current_app)

