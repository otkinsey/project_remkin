from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'event.views.home', name='home'),
    url(r'^dump/$', 'event.views.bigdump', name='dump'),
    url(r'^make/$', 'event.views.mkevent', name='make'),
    url(r'^newuser/$', 'event.views.newuser', name='newuser'),
    url(r'^login/$', 'event.views.fakelogin', name='login'),
    url(r'^obliviate/$', 'event.views.obliviate', name='obliviate'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
