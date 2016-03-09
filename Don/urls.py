from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'Don.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^don/', include('ovs.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
