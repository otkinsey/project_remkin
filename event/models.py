from django.db import models
from django.forms.models import model_to_dict
from django.contrib.auth.models import User
from django.contrib.auth.models import Group, Permission

from django.contrib import admin


# Create your models here.

    
class Profile(models.Model):
    image=models.FileField(upload_to='profiles')
    user = models.OneToOneField(User)

class Usercategory(models.Model):
    image=models.FileField(upload_to='groups')
    
    group=models.OneToOneField(Group)


class Location(models.Model):

    locationName= models.CharField(max_length=500)
    locationAddress=models.CharField(max_length=500)
    locationDescription = models.CharField(max_length=500)
    #Hours?
    #
    creator = models.ForeignKey(User)
    creationTime  = models.DateTimeField(auto_now_add=True)
    longitude = models.FloatField()
    latitude = models.FloatField()
    rsvps = models.CharField(max_length=500)
    def to_dict(self):
        return model_to_dict(self)





class Frontline(models.Model):
    email= models.CharField(max_length=500)
    fname = models.CharField(max_length=500)
    lname = models.CharField(max_length=500)
    organization = models.CharField(max_length=500)
    Comments = models.CharField(max_length=50000)
    creationTime  = models.DateTimeField(auto_now_add=True)
    def to_dict(self):
        return model_to_dict(self)


class Task(models.Model):
    taskTitle= models.CharField(max_length=500)
    assignments = models.ManyToManyField(User)
    subtasks = models.ManyToManyField("self", symmetrical=False)
    taskPriority = models.CharField(max_length=500)
    taskStatus=models.CharField(max_length=500)
    taskDuedate = models.CharField(max_length=500)
    taskCompletiondate = models.CharField(max_length=500)
    taskDescription = models.CharField(max_length=5000)
    creator = models.ForeignKey(User,related_name="taskCreator")
    creationTime  = models.DateTimeField(auto_now_add=True)
    def to_dict(self):
        return model_to_dict(self)




class Event(models.Model):
    eventName= models.CharField(max_length=500)
    eventStartTime = models.CharField(max_length=500)
    eventAddress=models.CharField(max_length=500)
    image=models.FileField(upload_to='events')
    
    eventDuration = models.CharField(max_length=500)
    eventDescription = models.CharField(max_length=5000)
    eventLocationDescription = models.CharField(max_length=500)
    longitude = models.FloatField()
    latitude = models.FloatField()
    creator = models.ForeignKey(User,related_name="eventCreator")
    creationTime  = models.DateTimeField(auto_now_add=True)
    eventComputedStartTime = models.DateTimeField()
    eventComputedEndTime = models.DateTimeField()
    EventRSVPS = models.ManyToManyField(User,related_name="eventrsvplist", blank=True)
    tasklist = models.ManyToManyField(Task)
    def to_dict(self):
        return model_to_dict(self)




#class EventAdmin Admin(admin.ModelAdmin):
#    list_display = ('eventName', 'eventAddress', 'creator')


admin.site.register(Event)

admin.site.register(Task)
admin.site.register(Frontline)

