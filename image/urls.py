from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from image.views import StreamView, UploadImageView, EditImageView


urlpatterns = patterns('',
    url(r'^stream/$', login_required(StreamView.as_view(
        template_name='stream.html')),
        name='stream'),
    url(r'^library/$', 'image.views.library_view', name='library'),
    url(r'^gallery/(?P<pk>\d+)$', 'image.views.gallery_view',
        name='gallery'),
    url(r'^upload_image/$', login_required(UploadImageView.as_view(
        template_name='upload_image.html')),
        name='upload_image'),
    url(r'^edit_image/(?P<pk>\d+)$', login_required(EditImageView.as_view(
        template_name='edit_image.html')),
        name='edit_image'),
    url(r'^image_page/(?P<pk>\d+)$', 'image.views.image_page',
        name='image_page'),
)
