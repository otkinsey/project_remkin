from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))



urlpatterns = patterns('',
    # Examples:
    url(r'^dump/$', 'event.views.bigdump', name='dump'),
    url(r'^search/$', 'event.views.search', name='search'),
    url(r'^taskdump/$', 'event.views.taskdump', name='taskdump'),
    url(r'^tasksearch/$', 'event.views.tasksearch', name='tasksearch'),

    url(r'^make/$', 'event.views.mkevent', name='make'),
    url(r'^eventupdate/$', 'event.views.eventupdate', name='eventupdate'),


    url(r'^maketask/$', 'event.views.mktask', name='maketask'),
    url(r'^mki/$', 'event.views.mki', name='mki'),


    url(r'^frontline/$', 'event.views.frontline', name='fakelogin'),

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

    url(r'^taskupdate/$', 'event.views.taskupdate', name='taskupdate'),

    url(r'^takeinterest/$', 'event.views.takeinterest', name='takeinterest'),
    url(r'^dropinterest/$', 'event.views.dropinterest', name='dropinterest'),


    url(r'^mkgroup/$', 'event.views.mkgroup', name='mkgroup'),
    url(r'^listgroups/$', 'event.views.listgroups', name='listgroups'),
    url(r'^joingroup/$', 'event.views.mkgroup', name='joingroup'),
    url(r'^leavegroup/$', 'event.views.mkgroup', name='leavegroup'),
    url(r'^kickgroup/$', 'event.views.mkgroup', name='kickgroup'),
    url(r'^addorgadmin/$', 'event.views.addorgadmin', name='addadmin'),
    url(r'^rmorgadmin/$', 'event.views.rmorgadmin', name='rmadmin'),
    
    url(r'^mkcomment/$', 'event.views.mkcomment', name='mkcomment'),
    url(r'^comments/$', 'event.views.comments', name='mkcomment'),
    url(r'^rmcomment/$', 'event.views.rmcomment', name='mkcomment'),


    url(r'^lookupuid/$', 'event.views.LookUpUid', name='luuid'),

    url(r'^lookupuser/$', 'event.views.LookUpUserName', name='luun'),

    url(r'^listinterests/$', 'event.views.listinterests', name='listinterests'),

    url(r'^eventimage/$', 'event.views.eventimage', name='eventimage'),
    url(r'^image/$', 'event.views.eventimage', name='eventimage'),
    url(r'^geteventimage/$', 'event.views.geteventimage', name='geteventimage'),
    url(r'^getimage/$', 'event.views.geteventimage', name='geteventimage'),

    url(r'^obliviate/$', 'event.views.obliviate', name='obliviate'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^bloorp/', include(admin.site.urls)),
    url(r'^blaap/(?P<path>.*)$', 'django.views.static.serve',        {'document_root': '/var/django/stylefiles'}),
    url(r'^$', 'event.views.homeindex', name='home'),
    url(r'^(?P<path>.*\.html)$', 'event.views.htmlserve', name='htmlserve' ),
    url(r'^(\d+)$', 'event.views.htmlevent',  name='htmlevent'),

    url(r'^(?P<path>.*)$', 'django.views.static.serve',        {'document_root': BASE_DIR+'/static'}),
)
