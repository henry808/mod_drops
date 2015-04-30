from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView
from image.models import Image
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect


class StreamView(ListView):
    model = Image
    template_name = "stream.html"


class UploadImage(CreateView):
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
                    'library',
                    kwargs={'pk': request.user.profile.pk}
                ))
        return self.render_to_response({'form': form})


class EditImage(UpdateView):
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
                    'library',
                    kwargs={'pk': instance.user.profile.pk}
                ))
        return self.render_to_response({'form': form})


@login_required
def library_view(request, *args, **kwargs):
    return render(request, 'library.html', {})
