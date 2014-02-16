from django.db import models
from django.forms.models import model_to_dict
from django.contrib.auth.models import User
from django.contrib.auth.models import Group, Permission

# Create your models here.

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


class Event(models.Model):
    eventName= models.CharField(max_length=500)
    eventStartTime = models.CharField(max_length=500)
    eventAddress=models.CharField(max_length=500)
    
    eventDuration = models.CharField(max_length=500)
    eventDescription = models.CharField(max_length=500)
    eventLocationDescription = models.CharField(max_length=500)
    
    creator = models.ForeignKey(User,related_name="eventCreator")
    creationTime  = models.DateTimeField(auto_now_add=True)
    eventComputedStartTime = models.DateTimeField(auto_now_add=True)
    eventComputedEndTime = models.DateTimeField(auto_now_add=True)
#    eventLocation = models.ForeignKey(Location)
    EventRSVPS = models.ManyToManyField(User,related_name="eventrsvplist")
    
class Task(models.Model):
    taskName= models.CharField(max_length=500)
    eventStartTime = models.CharField(max_length=500)
    eventAddress=models.CharField(max_length=500)
    
    eventDuration = models.CharField(max_length=500)
    eventDescription = models.CharField(max_length=500)
    eventLocationDescription = models.CharField(max_length=500)
    
    creator = models.ForeignKey(User,related_name="eventCreator")
    creationTime  = models.DateTimeField(auto_now_add=True)
    eventComputedStartTime = models.DateTimeField(auto_now_add=True)
    eventComputedEndTime = models.DateTimeField(auto_now_add=True)
#    eventLocation = models.ForeignKey(Location)
    EventRSVPS = models.ManyToManyField(User,related_name="eventrsvplist")
    

    def to_dict(self):
        return model_to_dict(self)
     #  return dict([(p, unicode(getattr(self, p))) for p in self.properties()])
    
            

