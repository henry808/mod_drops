from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^$', 'user_profile.views.profile', name='profile'),
    url(r'^update/(?P<pk>\d+)$', 'user_profile.views.profile_update_view',
        name='profile_update'),
]
