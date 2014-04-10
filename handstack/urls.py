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
    url(r'^frontline/$', 'event.views.frontline', name='fakelogin'),
    url(r'^fldump3224$', 'event.views.frontlinedump', name='fdump'),

    url(r'^register/$', 'event.views.userregister', name='registration'),
    url(r'^login/$', 'event.views.userlogin', name='login'),
    url(r'^logout/$', 'event.views.logout_view', name='logout'),
    url(r'^whoami/$', 'event.views.whoami', name='whoami'),

    url(r'^rsvp/$', 'event.views.rsvpme', name='rsvp'),
    url(r'^unrsvp/$', 'event.views.unrsvpme', name='unsrvp'),
    url(r'^myevents/$', 'event.views.myevents', name='myevents'),

    url(r'^taketask/$', 'event.views.taketask', name='taketask'),
    url(r'^droptask/$', 'event.views.droptask', name='droptask'),
    url(r'^mytasks/$', 'event.views.mytasks', name='mytasks'),
    url(r'^givetask/$', 'event.views.givetask', name='givetask'),

    url(r'^mkgroup/$', 'event.views.mkgroup', name='mkgroup'),



    url(r'^eventimage/$', 'event.views.eventimage', name='eventimage'),
    url(r'^geteventimage/$', 'event.views.geteventimage', name='geteventimage'),

    url(r'^obliviate/$', 'event.views.obliviate', name='obliviate'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^bloorp/', include(admin.site.urls)),
    url(r'^blaap/(?P<path>.*)$', 'django.views.static.serve',        {'document_root': '/var/django/stylefiles'}),

    url(r'^$', 'event.views.homeindex', name='home'),
    url(r'^(?P<path>.*\.html)$', 'event.views.htmlserve', ),

    url(r'^(?P<path>.*)$', 'django.views.static.serve',        {'document_root': '/var/django/handstack/static'}),

)
