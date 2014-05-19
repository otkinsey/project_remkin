from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse,Http404
from django.views.decorators.csrf import csrf_exempt
from django.db import models
from django.forms.models import model_to_dict
from django.contrib.auth.models import User,Group
from django.contrib.auth import authenticate, login
import json
import datetime
from django.contrib.auth import logout

from dateutil import parser

from models import Event,Location,Task,Profile,Frontline, Organization,Comment,Interest

from django.template import RequestContext, loader
import reversion


import magic  #wtf python




#  
# search/ by interest 
#  


def isadmin(user,e):
    ##if user in e.Organization.Admins.all() or user==e.Organization.creator or 
    if user.id==e.creator.id:
        return True
    return True

def dointerests(thisevent,intids):
    intlist = [int(x.strip()) for x in intids.split(',')]    
    data=dict()
    data["intlist"]=intlist
    for intid in intlist:
        i= get_object_or_404(Interest,id__exact=intid )



        thisevent.interests.add(i)    
        data[intid]="foo"
    thisevent.save()
    return data




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


def htmlserve(request,path,filename="thankyou.html"):
#    return HttpResponse("Hello, handstack.")
    template=loader.get_template(path)
    context = RequestContext(request, {
        'pageinfo': filename,
       })
    return HttpResponse(template.render(context))



def htmlevent(request,eid):
#    return HttpResponse("Hello, handstack.")
    template=loader.get_template("eventemplate.html")
    q=Event.objects
    tdata=dict()
    cdata=dict()

    q=q.filter(id=int(eid))

    for thing in q.all():
        cdata=thing.to_dict()

    context = RequestContext(request, cdata)
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

@csrf_exempt
def search(request):
    data=dict()
    cdata=dict()
    
    q=Event.objects
    latDist=1.0
    lonDist=1.0
    ringwdth=0.1
    qdata=dict()

    if 'eventid' in request.GET:
        q=q.filter(id=int(request.GET['eventid']) )

    if 'interest' in request.GET:
        q=q.filter(interests__group__name=request.GET['interest'])



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
    
    if 'ring' in request.GET:
        if 'latitude' in request.GET:
            lat=float(request.GET['latitude'])
        if 'longitude' in request.GET:
            lon=float(request.GET['longitude'])
        ring=float(request.GET['ring'])

    if 'latitude' in request.GET:
        lat=float(request.GET['latitude'])
        qdata['latitude']=lat

        q=q.filter(latitude__range=(lat-latDist, lat+latDist))
    if 'longitude' in request.GET:
        lon=float(request.GET['longitude'])
        qdata['longitude']=lon
        q=q.filter(longitude__range=(lon-lonDist, lon+lonDist))



    for thing in q.all():
        cdata[str(thing.id)]=thing.to_dict()
    data["events"]=cdata
    qdata['lonDist']=lonDist
    qdata['latDist']=latDist
    data['queryterms']=qdata
    data["success"]=True
    return HttpResponse(json.dumps(data, cls=ComplexEncoder),content_type="application/json")

def tasksearch(request):
    data=dict()
    cdata=dict()
    
    q=Event.objects

    if 'eventid' in request.GET:
        q=q.get(id__exact=int(request.GET['eventid']))
    for thing in q.tasklist.all():
        cdata[str(thing.id)]=thing.to_dict()
    data["tasks"]=cdata
    data["success"]=True
    return HttpResponse(json.dumps(data, cls=ComplexEncoder),content_type="application/json")




@reversion.create_revision()
@csrf_exempt
def rmtask(request):
    if request.user.is_authenticated() and "taskid" in request.GET:
        t=get_object_or_404(Task,id__exact=int(request.GET['taskid']))
        e=t.event_set.all()[0]
        if request.user.id == e.creator.id:
            t.delete()
    return HttpResponse('{"success": true}',content_type="application/json")



@reversion.create_revision()
@csrf_exempt
def rmevent(request):
    data=dict()
    if request.user.is_authenticated() and 'eventid' in request.GET:
        q=get_object_or_404(Event,id__exact=int(request.GET['eventid']))
        if request.user.id == q.creator.id:
            q.delete()
    data["success"]=True
    #Handle orphan tasks
    return HttpResponse(json.dumps(data, cls=ComplexEncoder),content_type="application/json")



@reversion.create_revision()
@csrf_exempt
def mkcomment(request):
    data=dict()
    if request.user.is_authenticated() and 'eventid' in request.POST:
        e=get_object_or_404(Event,id__exact=int(request.POST['eventid']))
        c=Comment()
        for field in request.POST:
            setattr(c,field, request.POST[field])
        c.author=request.user        
        c.lastedit=request.user
        c.parentEvent=e
        c.save()
        data["test"]="foo"

    #Handle orphan tasks
    data["comment"]=c.to_dict()
    data["success"]=True
    return HttpResponse(json.dumps(data, cls=ComplexEncoder),content_type="application/json")

##comment, reply, delete own message, admin delete.

@reversion.create_revision()
@csrf_exempt
def comments(request):
    data=dict()
    cdata=dict()
    c=Comment.objects
    if 'eventid' in request.GET:
        e=get_object_or_404(Event,id__exact=int(request.GET['eventid']))
        c=c.filter(parentEvent=e)
        for thing in c.all():
            cdata[str(thing.id)]=thing.to_dict()
        data["comments"]=cdata
    data["success"]=True
    return HttpResponse(json.dumps(data),content_type="application/json")


@reversion.create_revision()
@csrf_exempt
def rmcomment(request):
    data=dict()
    u=request.user
    if request.user.is_authenticated() and 'commentid' in request.GET:
        c=get_object_or_404(Comment,id__exact=int(request.GET['commentid']))
        if isadmin(u,c.parentEvent) or u==c.author:
            c.delete()
    data["success"]=True
    #Handle orphan tasks
    return HttpResponse(json.dumps(data, cls=ComplexEncoder),content_type="application/json")










@csrf_exempt
def rsvpme(request):
    data=dict()
    cdata=dict()
    q=Event.objects
    if request.user.is_authenticated():
        if 'eventid' in request.GET:
            q=q.get(id__exact=int(request.GET['eventid']))
            if not request.user.id in q.EventRSVPS.all():
                q.EventRSVPS.add(request.user)
                q.save()
        data["success"]=True
        return HttpResponse(json.dumps(data, cls=ComplexEncoder),content_type="application/json")
    else:
        data["success"]=False
        return HttpResponse(json.dumps(data, cls=ComplexEncoder),content_type="application/json")

@csrf_exempt
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



@csrf_exempt
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





@csrf_exempt
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




@reversion.create_revision()
@csrf_exempt
def taskupdate(request):
    data=dict()
    cdata=dict()
    t=Task.objects
    if request.user.is_authenticated():
        if 'taskid' in request.POST:
            t=t.get(id__exact=int(request.POST['taskid']))
            e=t.event_set.all()[0]
    #        data["E"]=e.to_dict()

            if request.user in e.EventRSVPS.all():
                data["member"]="ok"
                t.lastedit=request.user
                for field in request.POST:
                    setattr(t,field, request.POST[field])
                t.save()
        data["debug"]=request.POST["taskStatus"]
        data["debug2"]=t.taskStatus
        data["success"]=True
        data["T"]=t.to_dict()
        return HttpResponse(json.dumps(data, cls=ComplexEncoder),content_type="application/json")
    else:
        data["success"]=False
        return HttpResponse(json.dumps(data, cls=ComplexEncoder),content_type="application/json")

@reversion.create_revision()
@csrf_exempt
def orgupdate(request):
    data=dict()
    cdata=dict()
    t=Organization.objects
    if request.user.is_authenticated():
        if 'orgid' in request.POST:
            o=o.get(id__exact=int(request.POST['orgid']))
    #        data["E"]=e.to_dict()

            if request.user in o.Admins.all() or request.user==o.creator:
                data["member"]="ok"
                t.lastedit=request.user
                for field in request.POST:
                    setattr(t,field, request.POST[field])
                t.save()
        data["debug"]=request.POST["taskStatus"]
        data["debug2"]=t.taskStatus
        data["success"]=True
        data["T"]=t.to_dict()
        return HttpResponse(json.dumps(data, cls=ComplexEncoder),content_type="application/json")
    else:
        data["success"]=False
        return HttpResponse(json.dumps(data, cls=ComplexEncoder),content_type="application/json")


@reversion.create_revision()
@csrf_exempt
def eventupdate(request):
    data=dict()
    cdata=dict()
    e=Event.objects
    u=request.user
    if u.is_authenticated():
        if 'eventid' in request.POST:
            e=e.get(id__exact=int(request.POST['eventid']))
            if isadmin(u, e):
                data["member"]="ok"
                e.lastedit=request.user
                for field in request.POST:
                    if str(field) == "interests":
                        data["intids"]=dointerests(e,request.POST[field])
                    else:
                        setattr(e,field, request.POST[field])
                e.save()
        data["query"]=request.POST
        data["success"]=True
        data["event"]=e.to_dict()
        return HttpResponse(json.dumps(data, cls=ComplexEncoder),content_type="application/json")
    else:
        data["success"]=False
        return HttpResponse(json.dumps(data, cls=ComplexEncoder),content_type="application/json")





@csrf_exempt
def givetask(request):
    data=dict()
    cdata=dict()
    t=Task.objects
    u=User.objects
    if request.user.is_authenticated():
        if 'taskid' in request.POST and 'uid' in request.POST: 
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


@csrf_exempt
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


@csrf_exempt
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
 #   for thing in Event.objects.all():
 #       thing.delete()
 #   for thing in Task.objects.all():
 #       thing.delete()
    return HttpResponse('{"success": true}',content_type="application/json")



@csrf_exempt
def mkevent(request):
    newevent=Event();
    newevent.latitude=0.0
    newevent.longitude=0.0

    for field in request.POST:
        if str(field) == "interests":
            data["intids"]=dointerests(e,request.POST[field])
        else:
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
    if "eventid" in request.POST:
        e=Event.objects
        e=e.get(id__exact=int(request.POST['eventid'])) 
        form = UploadFileForm(request.POST, request.FILES)
        e.image=request.FILES['image']
        e.save()        
    if "orgid" in request.POST:
        e=Organization.objects
        e=e.get(id__exact=int(request.POST['orgid'])) 
        form = UploadFileForm(request.POST, request.FILES)
        e.image=request.FILES['image']
        e.save()        
    if "userid" in request.POST:
        e=Profile.objects
        e=e.get(user__id__exact=int(request.POST['userid'])) 
        form = UploadFileForm(request.POST, request.FILES)
        e.image=request.FILES['image']
        e.save()        
    
    data["success"]=True
    return HttpResponse(json.dumps(data),content_type="application/json")





@csrf_exempt
def geteventimage(request):
    if "eventid" in request.GET:
        e=get_object_or_404(Event,id__exact=int(request.GET['eventid']))
        if not e.image:
            raise Http404
        if "thumbnail" in request.GET:
            file=e.image_thumbnail
        else:
            file=e.image
        handle=file._get_file()
        data=handle.read()
        type=magic.from_buffer(data,mime=True)
    if "orgid" in request.GET:
        e=get_object_or_404(Organization,id__exact=int(request.GET['orgid']))
        if "thumbnail" in request.GET:
            file=e.image_thumbnail
        else:
            file=e.image
        handle=file._get_file()
        data=handle.read()
        type=magic.from_buffer(data,mime=True)
    if "userid" in request.GET:
        p=get_object_or_404(Profile,user__id__exact=int(request.GET['userid']))
        #p=get_object_or_404(Profile,user=u.id)
        
        if "thumbnail" in request.GET:
            file=p.image_thumbnail
        else:
            file=p.image
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
    template=loader.get_template('thankyou.html')
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
    newgroup,created=Group.objects.get_or_create(name=request.POST['name'])
    neworg=Organization()
    neworg.group=newgroup
    newgroup.save()
    for field in request.POST:
        setattr(neworg,field, request.POST[field])
    newgroup.user_set.add(user)

    neworg.creator=request.user
    neworg.save()
    neworg.Admins.add(user)
    newgroup.save()
    neworg.save()

    return HttpResponse('{"success": true, "orgid": ' + str(neworg.id) + '}',content_type="application/json")



@csrf_exempt
def mki(request):
    data=dict()
    interestlist=["Accessibility",
"Animals",
"Arts",
"Discrimination",
"Economy",
"Education",
"Environment",
"Faith",
"Women's Rights",
"Government",
"Health",
"Human Rights",
"Immigration",
"Labor",
"LGBTQIA",
"Mental Health",
"Prison System",
"Race",
"Technology",
"Transportation",
"Youth"]

    for intname in interestlist:
        newgroup,created=Group.objects.get_or_create(name=intname)
        newgroup.save()

        newint,created=Interest.objects.get_or_create(group=newgroup,creator=request.user)
        newint.group=newgroup

        newint.save()
        newgroup.save()
        data[intname]=intname
    data["success"]=True
    return HttpResponse(json.dumps(data, cls=ComplexEncoder),content_type="application/json")



#get group image (overload get user image)


@csrf_exempt
def listgroups(request):
    data=dict()
    o=Organization.objects   

    for thing in o.all():
        data[str(thing.id)]=thing.to_dict()
    
    data["success"]=True
    return HttpResponse(json.dumps(data, cls=ComplexEncoder),content_type="application/json")


@csrf_exempt
def listinterests(request):
    data=dict()
    o=Interest.objects   

    for thing in o.all():
        data[str(thing.id)]=thing.to_dict()
    
    data["success"]=True
    return HttpResponse(json.dumps(data, cls=ComplexEncoder),content_type="application/json")


@csrf_exempt
def joingroup(request):
    data=dict()
    data["success"]=True
    if request.user.is_authenticated():
        o=get_object_or_404(Organization,id__exact=int(request.GET['orgid']))
        o.group.user_set.add(request.user)    
    return HttpResponse(json.dumps(data),content_type="application/json")


@csrf_exempt
def leavegroup(request):
    data=dict()
    data["success"]=True
    if request.user.is_authenticated():
        o=get_object_or_404(Organization,id__exact=int(request.GET['orgid']))
        o.group.user_set.remove(request.user)
    return HttpResponse(json.dumps(data),content_type="application/json")


@csrf_exempt
def joingroup(request):
    data=dict()
    data["success"]=True
    if request.user.is_authenticated():
        o=get_object_or_404(Organization,id__exact=int(request.GET['orgid']))
        o.group.user_set.add(request.user)
    return HttpResponse(json.dumps(data),content_type="application/json")


@csrf_exempt
def leavegroup(request):
    data=dict()
    data["success"]=True
    if request.user.is_authenticated():
        o=get_object_or_404(Organization,id__exact=int(request.GET['orgid']))
        o.group.user_set.remove(request.user)
    return HttpResponse(json.dumps(data),content_type="application/json")


@csrf_exempt
def takeinterest(request):
    data=dict()
    data["success"]=True
    if request.user.is_authenticated():
        o=get_object_or_404(Interest,id__exact=int(request.GET['intid']))
        o.group.user_set.add(request.user)
    return HttpResponse(json.dumps(data),content_type="application/json")


@csrf_exempt
def dropinterest(request):
    data=dict()
    data["success"]=True
    if request.user.is_authenticated():
        o=get_object_or_404(Interest,id__exact=int(request.GET['intid']))
        o.group.user_set.remove(request.user)
    return HttpResponse(json.dumps(data),content_type="application/json")








@csrf_exempt
def kickuserfromgroup(request):
    data=dict()
    data["success"]=True
    o=get_object_or_404(Organization,id__exact=int(request.GET['orgid']))

    if request.user.is_authenticated() and request.user in o.Admins.all():
        u=get_object_or_40(User,id__exact=int(request.GET['uid']))
        o.group.user_set.remove(u)

    return HttpResponse(json.dumps(data),content_type="application/json")



@csrf_exempt
def addorgadmin(request):
    data=dict()
    data["success"]=True
    if request.user.is_authenticated():
        o=get_object_or_404(Organization,id__exact=int(request.GET['orgid']))
        if request.user.is_authenticated() and request.user in o.Admins.all() or request.user==o.creator:
            o.Admins.add(request.user)
    return HttpResponse(json.dumps(data),content_type="application/json")


@csrf_exempt
def rmorgadmin(request):
    data=dict()
    data["success"]=True
    o=get_object_or_404(Organization,id__exact=int(request.GET['orgid']))

    if request.user.is_authenticated() and request.user in o.Admins.all() or request.user==o.creator:
        u=get_object_or_40(User,id__exact=int(request.GET['uid']))
        o.group.user_set.remove(u)

    return HttpResponse(json.dumps(data),content_type="application/json")







@csrf_exempt
def LookUpUid(request):
    data=dict()
    for field in request.GET:
        try:
            user = User.objects.get(id__exact=int(request.GET[field]))
        except User.DoesNotExist:
            data[request.GET[field]]=-1
            data["success"]=True
        data[request.GET[field]]=user.username
    return HttpResponse(json.dumps(data),content_type="application/json")



@csrf_exempt
def LookUpUserName(request):
    data=dict()
    try:
        user = User.objects.get(username=request.GET['username'])
    except User.DoesNotExist:
        data["uid"]=-1
        data["success"]=True
        return HttpResponse(json.dumps(data),content_type="application/json")
    data["success"]=True
    data["uid"]=user.id
    return HttpResponse(json.dumps(data),content_type="application/json")






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


#Registration name lookup

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

