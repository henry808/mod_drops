from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^$', 'mod_drops.views.index', name='index'),
    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^profile/', include('user_profile.urls'), namespace='profile'),

    url(r'^admin/', include(admin.site.urls)),
]
