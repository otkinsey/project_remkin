from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^dump/$', 'event.views.bigdump', name='dump'),
    url(r'^search/$', 'event.views.search', name='search'),
    url(r'^taskdump/$', 'event.views.taskdump', name='taskdump'),
    url(r'^tasksearch/$', 'event.views.tasksearch', name='tasksearch'),
    url(r'^make/$', 'event.views.mkevent', name='make'),
    url(r'^maketask/$', 'event.views.mktask', name='maketask'),
    url(r'^fakeuser/$', 'event.views.newuser', name='newuser'),
    url(r'^fakelogin/$', 'event.views.fakelogin', name='fakelogin'),
    url(r'^frontline/$', 'event.views.frontline', name='fakelogin'),
    url(r'^fldump3224$', 'event.views.frontlinedump', name='fdump'),

    url(r'^register/$', 'event.views.userregister', name='registration'),
    url(r'^login/$', 'event.views.userlogin', name='login'),
    url(r'^logout/$', 'event.views.logout_view', name='logout'),
    url(r'^whoami/$', 'event.views.whoami', name='whoami'),

    url(r'^obliviate/$', 'event.views.obliviate', name='obliviate'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', 'event.views.homeindex', name='home'),
    url(r'^(?P<path>.*)$', 'django.views.static.serve',        {'document_root': '/var/django/handstack/static'}),

    url(r'^admin/', include(admin.site.urls)),
)
