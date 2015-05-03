from django.conf.urls import include, url
from django.contrib import admin
from user_profile.views import OtherUsersView
from django.contrib.auth.decorators import login_required

urlpatterns = [
    url(r'^other_users/$', login_required(OtherUsersView.as_view(
                               template_name='other_users.html')),
                           name='other_users'),
    url(r'^$', 'user_profile.views.profile', name='profile'),
    url(r'^update/(?P<pk>\d+)$', 'user_profile.views.profile_update',
        name='profile_update'),
]
