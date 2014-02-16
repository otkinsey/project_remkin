from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from models import Event,Location
import json
from django.db import models
from django.forms.models import model_to_dict

from django.contrib.auth.models import User

from django.contrib.auth import authenticate, login
# Create your views here.
def home(request):
    return HttpResponse("Hello, handstack.")


def bigdump(request):
    data=dict()
    cdata=dict()
    for thing in Event.objects.all():
        cdata[str(thing.id)]=thing.to_dict()
    data["events"]=cdata
    data["success"]=True
    return HttpResponse(json.dumps(data),content_type="application/json")
    

def obliviate(request):
    for thing in Event.objects.all():
        thing.delete()
    return HttpResponse('{"success": true}',content_type="application/json")

@csrf_exempt
def mkevent(request):
    newevent=Event();
    for field in request.POST:
        setattr(newevent,field, request.POST[field])
    user = authenticate(username='testuser', password='8jfkldsa8uew8')
    newevent.creator=user
    newevent.save()
    return HttpResponse('{"success": true, "id": ' + str(newevent.id) + '}',content_type="application/json")

def newuser(request):
    user = User.objects.create_user('testuser', 'james.andrix+user@gmail.com', '8jfkldsa8uew8')
    return HttpResponse('{"success": true}',content_type="application/json")

def fakelogin(request):
    user = authenticate(username='testuser', password='8jfkldsa8uew8')
    login(request, user)
    return HttpResponse('{"success": true}',content_type="application/json")

