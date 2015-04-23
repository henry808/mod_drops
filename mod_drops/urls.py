from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^$', 'mod_drops.views.index', name='index'),
    # Examples:
    # url(r'^$', 'mod_drops.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
]
