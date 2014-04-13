from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import models
from django.forms.models import model_to_dict
from django.contrib.auth.models import User,Group
from django.contrib.auth import authenticate, login
import json
import datetime
from django.contrib.auth import logout

from dateutil import parser

from models import Event,Location,Task,Profile,Usercategory,Frontline

from django.template import RequestContext, loader


# Create your views here.


class ComplexEncoder(json.JSONEncoder):
    def default(self, obj):
        try:
            return super(ComplexEncoder, obj).default(obj)
        except TypeError:
            return str(obj)


def homeindex(request):
#    return HttpResponse("Hello, handstack.")
    template=loader.get_template('home.html')
    context = RequestContext(request, {
        'pageinfo': 5,
       })
    return HttpResponse(template.render(context))


def htmlserve(request,path,filename="template.html"):
#    return HttpResponse("Hello, handstack.")
    template=loader.get_template(path)
    context = RequestContext(request, {
        'pageinfo': filename,
       })
    return HttpResponse(template.render(context))



def bigdump(request):
    data=dict()
    cdata=dict()
    for thing in Event.objects.all():
        cdata[str(thing.id)]=thing.to_dict()
    data["events"]=cdata
    data["success"]=True
    return HttpResponse(json.dumps(data),content_type="application/json")



def frontlinedump(request):
    data=dict()
    cdata=dict()
    if 'code' in request.GET and request.GET["code"]=="frob":
        for thing in Frontline.objects.all():
            cdata[str(thing.id)]=thing.to_dict()
        data["contacts"]=cdata
        data["success"]=True
    else:
        data["success"]=True
    return HttpResponse(json.dumps(data),content_type="application/json")



def taskdump(request):
    data=dict()
    cdata=dict()
    for thing in Task.objects.all():
        cdata[str(thing.id)]=thing.to_dict()
    data["events"]=cdata
    data["success"]=True
    return HttpResponse(json.dumps(data),content_type="application/json")

def search(request):
    data=dict()
    cdata=dict()
    
    q=Event.objects
    latDist=0.1
    lonDist=0.1

    if 'eventid' in request.GET:
        q=q.filter(id=int(request.GET['eventid']) )

    if 'latDist' in request.GET:
        latDist=float(request.GET['latDist'])
    if 'lonDist' in request.GET:
        lonDist=float(request.GET['lonDist'])

    if 'startafter' in request.GET:
        startafter=request.GET['startafter']
        q=q.filter(eventComputedStartTime__gt=parser.parse(startafter))

    if 'startbefore' in request.GET:
        startbefore=request.GET['startbefore']
        q=q.filter(eventComputedStartTime__lt=parser.parse(startbefore))

    if 'latitude' in request.GET:
        lat=float(request.GET['latitude'])
        q=q.filter(latitude__range=(lat-latDist, lat+latDist))
    if 'longitude' in request.GET:
        lon=float(request.GET['longitude'])
        q=q.filter(longitude__range=(lon-lonDist, lon+lonDist))
    for thing in q.all():
        cdata[str(thing.id)]=thing.to_dict()
    data["events"]=cdata
    data["success"]=True
    return HttpResponse(json.dumps(data, cls=ComplexEncoder),content_type="application/json")

def tasksearch(request):
    data=dict()
    cdata=dict()
    
    q=Event.objects
    latDist=0.1
    lonDist=0.1

    if 'eventid' in request.GET:
        q=q.get(id__exact=int(request.GET['eventid']))
    for thing in q.tasklist.all():
        cdata[str(thing.id)]=thing.to_dict()
    data["tasks"]=cdata
    data["success"]=True
    return HttpResponse(json.dumps(data, cls=ComplexEncoder),content_type="application/json")

#Modify models too
def rmtask(request):
    return HttpResponse('{"success": true}',content_type="application/json")

def rmevent(request):
    q=Event.objects
    #If Permission
    if 'eventid' in request.GET:
        q=q.get(id__exact=int(request.GET['eventid']))
    
    q.hidemode=1
    q.save()
    data["success"]=True
    #Handle orphan tasks
    return HttpResponse(json.dumps(data, cls=ComplexEncoder),content_type="application/json")


def rsvpme(request):
    data=dict()
    cdata=dict()
    q=Event.objects
    if request.user.is_authenticated():
        if 'eventid' in request.POST:
            q=q.get(id__exact=int(request.POST['eventid']))
            if not request.user.id in q.EventRSVPS.all():
                q.EventRSVPS.add(request.user)
                q.save()
        data["success"]=True
        return HttpResponse(json.dumps(data, cls=ComplexEncoder),content_type="application/json")
    else:
        data["success"]=False
        return HttpResponse(json.dumps(data, cls=ComplexEncoder),content_type="application/json")


def unrsvpme(request):
    data=dict()

    bdata=dict()
    cdata=dict()
    q=Event.objects
    if request.user.is_authenticated():
        if 'eventid' in request.POST:
            q=q.get(id__exact=int(request.POST['eventid']))
            q.EventRSVPS.remove(request.user)
            q.save()
        data["success"]=True
        return HttpResponse(json.dumps(data, cls=ComplexEncoder),content_type="application/json")
    else:
        data["success"]=False
        return HttpResponse(json.dumps(data, cls=ComplexEncoder),content_type="application/json")


def myevents(request):
    data=dict()
    cdata=dict()
    bdata=dict()
    
    q=Event.objects
    if request.user.is_authenticated():
        q=request.user.eventrsvplist

        data["success"]=True
        for thing in q.all():
            cdata[str(thing.id)]=thing.to_dict()
        data["eventrsvplist"]=cdata
        return HttpResponse(json.dumps(data, cls=ComplexEncoder),content_type="application/json")
    else:
        data["success"]=False
        return HttpResponse(json.dumps(data, cls=ComplexEncoder),content_type="application/json")





def taketask(request):
    data=dict()
    cdata=dict()
    q=Task.objects
    if request.user.is_authenticated():
        if 'taskid' in request.POST:
            q=q.get(id__exact=int(request.POST['taskid']))
            if not request.user.id in q.assignments.all():
                q.assignments.add(request.user)
                q.save()
        data["success"]=True
        return HttpResponse(json.dumps(data, cls=ComplexEncoder),content_type="application/json")
    else:
        data["success"]=False
        return HttpResponse(json.dumps(data, cls=ComplexEncoder),content_type="application/json")






def givetask(request):
    data=dict()
    cdata=dict()
    t=Task.objects
    u=User.objects
    if request.user.is_authenticated():
        if 'taskid' in request.GET and 'uid' in request.POST: 
            t=t.get(id__exact=int(request.POST['taskid']))
            u=u.get(id__exact=int(request.POST['userid']))
            e=t.event_set.all()[0]
            data["E"]=e.to_dict()

            if request.user.id == e.creator.id:
                data["owner"]="ok"
                t.assignments.add(u)
                t.save()
        data["success"]=True
        return HttpResponse(json.dumps(data, cls=ComplexEncoder),content_type="application/json")
    else:
        data["success"]=False
        return HttpResponse(json.dumps(data, cls=ComplexEncoder),content_type="application/json")


def droptask(request):
    data=dict()

    cdata=dict()
    q=Task.objects
    if request.user.is_authenticated():
        if 'taskid' in request.GET:
            q=q.get(id__exact=int(request.GET['taskid']))
            q.assignments.remove(request.user)
            q.save()
        data["success"]=True
        return HttpResponse(json.dumps(data, cls=ComplexEncoder),content_type="application/json")
    else:
        data["success"]=False
        return HttpResponse(json.dumps(data, cls=ComplexEncoder),content_type="application/json")


def mytasks(request):
    data=dict()
    cdata=dict()
    
    q=Task.objects
    if request.user.is_authenticated():
        q=request.user.task_set

        data["success"]=True
        for thing in q.all():
            cdata[str(thing.id)]=thing.to_dict()
        data["tasklist"]=cdata
        return HttpResponse(json.dumps(data, cls=ComplexEncoder),content_type="application/json")
    else:
        data["success"]=False
        return HttpResponse(json.dumps(data, cls=ComplexEncoder),content_type="application/json")










def blockuser(request):
    return HttpResponse('{"success": true}',content_type="application/json")
    
def obliviate(request):
    #If user=admin
    for thing in Event.objects.all():
        thing.delete()
    for thing in Task.objects.all():
        thing.delete()
    return HttpResponse('{"success": true}',content_type="application/json")

@csrf_exempt
def mkevent(request):
    newevent=Event();
    newevent.latitude=0.0
    newevent.longitude=0.0

    for field in request.POST:
        setattr(newevent,field, request.POST[field])
    if request.user.is_authenticated():
        newevent.creator=request.user
        newevent.eventComputedStartTime=parser.parse(newevent.eventStartTime)
        newevent.eventComputedEndTime=newevent.eventComputedStartTime + datetime.timedelta(seconds=int(float(newevent.eventDuration)))
        newevent.save()
        newevent.EventRSVPS.add(request.user)
        newevent.save()

    else:    
        return HttpResponse('{"success": false }',content_type="application/json")

    return HttpResponse('{"success": true, "id": ' + str(newevent.id) + '}',content_type="application/json")



from django import forms

class UploadFileForm(forms.Form):
    eventid = forms.CharField(max_length=50)
    eventimage = forms.FileField()



@csrf_exempt
def eventimage(request):
    data=dict()
    e=Event.objects
    e=e.get(id__exact=int(request.POST['eventid'])) 
    form = UploadFileForm(request.POST, request.FILES)
    e.image=request.FILES['eventimage']
    e.save()        
    data["success"]=True
    return HttpResponse(json.dumps(data),content_type="application/json")


import magic  #wtf python


@csrf_exempt
def geteventimage(request):
    
    e=Event.objects
    e=e.get(id__exact=int(request.GET['eventid']))
    
    file=e.image
    handle=file._get_file()
    data=handle.read()
    
    type=magic.from_buffer(data,mime=True)
    return HttpResponse(data,content_type=type)









@csrf_exempt
def frontline(request):
    newF=Frontline();
    for field in request.POST:
        setattr(newF,field, request.POST[field])
    #get event
    newF.save()
    template=loader.get_template('template.html')
    context = RequestContext(request, {
        'pageinfo': "We appreciate your interest. ",
       })
    return HttpResponse(template.render(context))







@csrf_exempt
def mktask(request):
    newtask=Task();
    for field in request.POST:
        setattr(newtask,field, request.POST[field])
    user = request.user
    newtask.creator=user
    newtask.save()
    #get event
    parentevent=Event.objects.get(id__exact=int(request.POST['eventid']))
    #add task to tasklist
    parentevent.tasklist.add(newtask)
    #save event
    parentevent.save()    
    return HttpResponse('{"success": true, "id": ' + str(newtask.id) + ', "eventName": "' + str(parentevent.eventName) + '"}',content_type="application/json")


@csrf_exempt
def mkgroup(request):
    user = request.user
    newgroup,created=Group.objects.get_or_create(name=request.GET['name'])
    newcat=Usercategory()
    newcat.group=newgroup
    newgroup.save()

    newgroup.user_set.add(user)
    
    newgroup.save()
    newcat.save()
    return HttpResponse('{"success": true, "gid": ' + str(newcat.id) + '}',content_type="application/json")






def logout_view(request):
    logout(request)
    data=dict();
    data["success"]=True
    return HttpResponse(json.dumps(data, cls=ComplexEncoder),content_type="application/json")

def whoami(request):
    data=dict();
    if request.user.is_authenticated():
        data["success"]=True
        data["uid"]=request.user.id
        return HttpResponse(json.dumps(data, cls=ComplexEncoder),content_type="application/json")
    else:
        data["success"]=True
        data["uid"]=-1
        return HttpResponse(json.dumps(data, cls=ComplexEncoder),content_type="application/json")




#Registration Form

#static

#Registration name lookup

#Registration Handler

@csrf_exempt
def userregister(request):
    email=request.POST['email']
    pword=request.POST['pword']
    uname=request.POST['username']
    data=dict();
    #test for already registered
    
    newuser = User.objects.create_user(uname, email, pword)
    user = authenticate(username=uname, password=pword)
    login(request, user)

    profile=Profile()
    profile.user=user
    profile.save()

    data["success"]=True
    data["uid"]=str(user.id)

    return HttpResponse(json.dumps(data, cls=ComplexEncoder),content_type="application/json")
    

#Login Form

#static


#login Handler
@csrf_exempt
def userlogin(request):
    pword=request.POST['pword']
    uname=request.POST['username']

    thisuser = authenticate(username=uname, password=pword)

    data=dict()
    if not thisuser or not thisuser.is_active:
        data["success"]=False
        data["reason"]="Authentication failed."
        return HttpResponse(json.dumps(data, cls=ComplexEncoder),content_type="application/json")
    else:
        login(request, thisuser)
        data["success"]=True
        data["uid"]=thisuser.id
        return HttpResponse(json.dumps(data, cls=ComplexEncoder),content_type="application/json")

