from django.shortcuts import render
from django.http import HttpResponse

from models import Event,Location
import json
from django.db import models
from django.forms.models import model_to_dict


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

def mkevent(request):
    newevent=Event();
    for field in request.GET:
        setattr(newevent,field, request.GET[field])
    newevent.save()
    return HttpResponse('{"success": true}',content_type="application/json")
