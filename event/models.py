from django.db import models
from django.forms.models import model_to_dict
from django.contrib.auth.models import User
from django.contrib.auth.models import Group, Permission

from django.contrib import admin

from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill

from reversion.helpers import patch_admin

# Create your models here.

    
class Profile(models.Model):
    image=models.FileField(upload_to='profiles')
    image_thumbnail =ImageSpecField(source='image',
                                      processors=[ResizeToFill(100, 100)],
                                      format='JPEG',
                                      options={'quality': 90})
    user = models.OneToOneField(User)


class Usercategory(models.Model):
    image=models.FileField(upload_to='groups')
    image_thumbnail =ImageSpecField(source='image',
                                      processors=[ResizeToFill(100, 100)],
                                      format='JPEG',
                                      options={'quality': 90})
    group=models.OneToOneField(Group)
    description = models.CharField(max_length=50000, default=" ")    
    lastedit = models.ForeignKey(User,related_name="categoryLastedit",blank=True,null=True)
    def to_dict(self):
        grp= model_to_dict(self.group)
        cat= model_to_dict(self)
        cat['group']=grp
        cat['name']=self.group.name
        return cat
    def __str__(self):
        return self.group.name


class Organization(Usercategory):
    orgAddress=models.CharField(max_length=500, blank=True,null=True)
    orgLocationDescription = models.CharField(max_length=500, blank=True,null=True)
    longitude = models.FloatField( blank=True,null=True)
    latitude = models.FloatField(blank=True,null=True)
    Admins= models.ManyToManyField(User,related_name="OrgAdmin", blank=True)
    creator = models.ForeignKey(User)

class Interest(Usercategory):
    creator = models.ForeignKey(User)
    hashtag = models.CharField(max_length=500)



class Location(models.Model):
    locationName= models.CharField(max_length=500)
    locationAddress=models.CharField(max_length=500)
    locationDescription = models.CharField(max_length=500)
    #Hours?
    #
    lastedit = models.ForeignKey(User,related_name="LocationLastedit",blank=True,null=True)
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
    def __str__(self):
        return self.email


class Task(models.Model):
    taskTitle= models.CharField(max_length=500)
    assignments = models.ManyToManyField(User)
    subtasks = models.ManyToManyField("self", symmetrical=False)
    taskPriority = models.CharField(max_length=500)
    taskStatus=models.CharField(max_length=500)
    taskDuedate = models.CharField(max_length=500)
    taskCompletiondate = models.CharField(max_length=500)
    taskDescription = models.CharField(max_length=5000)
    lastedit = models.ForeignKey(User,related_name="taskLastedit",blank=True,null=True)
    creator = models.ForeignKey(User,related_name="taskCreator")
    creationTime  = models.DateTimeField(auto_now_add=True)
    def to_dict(self):
        return model_to_dict(self)
    def __str__(self):
        return self.taskTitle



class Event(models.Model):
    eventName= models.CharField(max_length=500)
    eventStartTime = models.CharField(max_length=500)
    eventAddress=models.CharField(max_length=500)
    image=models.FileField(upload_to='events')
    image_thumbnail =ImageSpecField(source='image',
                                      processors=[ResizeToFill(494, 180)],
                                      format='JPEG',
                                      options={'quality': 90})
    eventDuration = models.CharField(max_length=500)
    eventDescription = models.CharField(max_length=5000)
    eventLocationDescription = models.CharField(max_length=500)
    longitude = models.FloatField()
    latitude = models.FloatField()
    creator = models.ForeignKey(User,related_name="eventCreator")
    lastedit = models.ForeignKey(User,related_name="eventLastedit",blank=True,null=True)
    Organizations = models.ManyToManyField(Organization)
    creationTime  = models.DateTimeField(auto_now_add=True)
    eventComputedStartTime = models.DateTimeField()
    eventComputedEndTime = models.DateTimeField()
    EventRSVPS = models.ManyToManyField(User,related_name="eventrsvplist", blank=True)
    EventCheckins = models.ManyToManyField(User,related_name="eventCheckins", blank=True)
    tasklist = models.ManyToManyField(Task)
    interests = models.ManyToManyField(Interest)

    def to_dict(self):
        return model_to_dict(self)
    def __str__(self):
        return self.eventName



class Comment(models.Model):
    body = models.CharField(max_length=50000)    
    author=models.ForeignKey(User)
    creationTime  = models.DateTimeField(auto_now_add=True)
    lastedit = models.ForeignKey(User,related_name="commentLastedit")
    parentEvent=models.ForeignKey(Event)
    def to_dict(self):
        return model_to_dict(self)
    def __str__(self):
        return self.author.username



#class EventAdmin Admin(admin.ModelAdmin):
#    list_display = ('eventName', 'eventAddress', 'creator')

admin.site.register(Frontline)

admin.site.register(Event)
patch_admin(Event)

admin.site.register(Task)
patch_admin(Task)

admin.site.register(Organization)
patch_admin(Organization)

admin.site.register(Usercategory)
patch_admin(Usercategory)

admin.site.register(Profile)
patch_admin(Profile)

admin.site.register(Comment)
patch_admin(Comment)

admin.site.register(Interest)
patch_admin(Interest)
