from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import models
from django.forms.models import model_to_dict
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
import json
import datetime
from django.contrib.auth import logout

from dateutil import parser

from models import Event,Location,Task,Profile,Usercategory


# Create your views here.

class ComplexEncoder(json.JSONEncoder):
    def default(self, obj):
        try:
            return super(ComplexEncoder, obj).default(obj)
        except TypeError:
            return str(obj)


def homeindex(request):
    return HttpResponse("Hello, handstack.")


def bigdump(request):
    data=dict()
    cdata=dict()
    for thing in Event.objects.all():
        cdata[str(thing.id)]=thing.to_dict()
    data["events"]=cdata
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
    return HttpResponse('{"success": true}',content_type="application/json")

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
        return HttpResponse('{"success": false }',content_type="application/json")
    else:    
        newevent.creator=request.user
        newevent.eventComputedStartTime=parser.parse(newevent.eventStartTime)
        newevent.eventComputedEndTime=newevent.eventComputedStartTime + datetime.timedelta(seconds=int(float(newevent.eventDuration)))

#    newevent.EventRSVPS=[user]
        newevent.save()
        return HttpResponse('{"success": true, "id": ' + str(newevent.id) + '}',content_type="application/json")






@csrf_exempt
def mktask(request):
    newtask=Task();
    for field in request.POST:
        setattr(newtask,field, request.POST[field])
    user = authenticate(username='testuser', password='8jfkldsa8uew8')
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
    newtask=Task();
    for field in request.POST:
        setattr(newtask,field, request.POST[field])
    user = authenticate(username='testuser', password='8jfkldsa8uew8')
    newtask.creator=user
    newtask.save()
    #get event
    parentevent=Event.objects.get(id__exact=int(request.POST['eventid']))
    #add task to tasklist
    parentevent.tasklist.add(newtask)
    #save event
    parentevent.save()
    return HttpResponse('{"success": true, "id": ' + str(newtask.id) + ', "eventName": "' + str(parentevent.eventName) + '"}',content_type="application/json")



def newuser(request):
    user = User.objects.create_user('testuser', 'james.andrix+user@gmail.com', '8jfkldsa8uew8')
    return HttpResponse('{"success": true}',content_type="application/json")





def fakelogin(request):
    user = authenticate(username='testuser', password='8jfkldsa8uew8')
    login(request, user)
    return HttpResponse('{"success": true}',content_type="application/json")



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
        data["success"]=False
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

