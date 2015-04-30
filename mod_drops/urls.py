from django.conf.urls import include, url, patterns
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = patterns('',
    url(r'^$', 'mod_drops.views.index', name='index'),
    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^profile/', include('user_profile.urls', namespace='profile')),
    url(r'^image/', include('image.urls', namespace='image')),

    url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
