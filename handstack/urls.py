from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^dump/$', 'event.views.bigdump', name='dump'),
    url(r'^search/$', 'event.views.search', name='search'),
    url(r'^taskdump/$', 'event.views.taskdump', name='taskdump'),
    url(r'^make/$', 'event.views.mkevent', name='make'),
    url(r'^maketask/$', 'event.views.mktask', name='maketask'),
    url(r'^newuser/$', 'event.views.newuser', name='newuser'),
    url(r'^login/$', 'event.views.fakelogin', name='login'),
    url(r'^obliviate/$', 'event.views.obliviate', name='obliviate'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^(?P<path>.*)$', 'django.views.static.serve',        {'document_root': '/var/django/handstack/static'}),

    url(r'^admin/', include(admin.site.urls)),
)
