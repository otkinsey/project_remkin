from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'events.views.home', name='home'),
    url(r'^dump/$', 'events.views.bigdump', name='dump'),
    url(r'^make/$', 'events.views.mkevent', name='make'),
    url(r'^obliviate/$', 'events.views.home', name='obliviate'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
