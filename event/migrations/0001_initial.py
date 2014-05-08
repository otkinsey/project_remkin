# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Profile'
        db.create_table(u'event_profile', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('image', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
        ))
        db.send_create_signal(u'event', ['Profile'])

        # Adding model 'Usercategory'
        db.create_table(u'event_usercategory', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('image', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('group', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.Group'], unique=True)),
        ))
        db.send_create_signal(u'event', ['Usercategory'])

        # Adding model 'Location'
        db.create_table(u'event_location', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('locationName', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('locationAddress', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('locationDescription', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('creationTime', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('longitude', self.gf('django.db.models.fields.FloatField')()),
            ('latitude', self.gf('django.db.models.fields.FloatField')()),
            ('rsvps', self.gf('django.db.models.fields.CharField')(max_length=500)),
        ))
        db.send_create_signal(u'event', ['Location'])

        # Adding model 'Frontline'
        db.create_table(u'event_frontline', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('email', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('fname', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('lname', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('organization', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('Comments', self.gf('django.db.models.fields.CharField')(max_length=50000)),
            ('creationTime', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'event', ['Frontline'])

        # Adding model 'Task'
        db.create_table(u'event_task', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('taskTitle', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('taskPriority', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('taskStatus', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('taskDuedate', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('taskCompletiondate', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('taskDescription', self.gf('django.db.models.fields.CharField')(max_length=5000)),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(related_name='taskCreator', to=orm['auth.User'])),
            ('creationTime', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'event', ['Task'])

        # Adding M2M table for field assignments on 'Task'
        m2m_table_name = db.shorten_name(u'event_task_assignments')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('task', models.ForeignKey(orm[u'event.task'], null=False)),
            ('user', models.ForeignKey(orm[u'auth.user'], null=False))
        ))
        db.create_unique(m2m_table_name, ['task_id', 'user_id'])

        # Adding M2M table for field subtasks on 'Task'
        m2m_table_name = db.shorten_name(u'event_task_subtasks')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_task', models.ForeignKey(orm[u'event.task'], null=False)),
            ('to_task', models.ForeignKey(orm[u'event.task'], null=False))
        ))
        db.create_unique(m2m_table_name, ['from_task_id', 'to_task_id'])

        # Adding model 'Event'
        db.create_table(u'event_event', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('eventName', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('eventStartTime', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('eventAddress', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('image', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('eventDuration', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('eventDescription', self.gf('django.db.models.fields.CharField')(max_length=5000)),
            ('eventLocationDescription', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('longitude', self.gf('django.db.models.fields.FloatField')()),
            ('latitude', self.gf('django.db.models.fields.FloatField')()),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(related_name='eventCreator', to=orm['auth.User'])),
            ('creationTime', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('eventComputedStartTime', self.gf('django.db.models.fields.DateTimeField')()),
            ('eventComputedEndTime', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'event', ['Event'])

        # Adding M2M table for field EventRSVPS on 'Event'
        m2m_table_name = db.shorten_name(u'event_event_EventRSVPS')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('event', models.ForeignKey(orm[u'event.event'], null=False)),
            ('user', models.ForeignKey(orm[u'auth.user'], null=False))
        ))
        db.create_unique(m2m_table_name, ['event_id', 'user_id'])

        # Adding M2M table for field tasklist on 'Event'
        m2m_table_name = db.shorten_name(u'event_event_tasklist')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('event', models.ForeignKey(orm[u'event.event'], null=False)),
            ('task', models.ForeignKey(orm[u'event.task'], null=False))
        ))
        db.create_unique(m2m_table_name, ['event_id', 'task_id'])


    def backwards(self, orm):
        # Deleting model 'Profile'
        db.delete_table(u'event_profile')

        # Deleting model 'Usercategory'
        db.delete_table(u'event_usercategory')

        # Deleting model 'Location'
        db.delete_table(u'event_location')

        # Deleting model 'Frontline'
        db.delete_table(u'event_frontline')

        # Deleting model 'Task'
        db.delete_table(u'event_task')

        # Removing M2M table for field assignments on 'Task'
        db.delete_table(db.shorten_name(u'event_task_assignments'))

        # Removing M2M table for field subtasks on 'Task'
        db.delete_table(db.shorten_name(u'event_task_subtasks'))

        # Deleting model 'Event'
        db.delete_table(u'event_event')

        # Removing M2M table for field EventRSVPS on 'Event'
        db.delete_table(db.shorten_name(u'event_event_EventRSVPS'))

        # Removing M2M table for field tasklist on 'Event'
        db.delete_table(db.shorten_name(u'event_event_tasklist'))


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'event.event': {
            'EventRSVPS': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'eventrsvplist'", 'blank': 'True', 'to': u"orm['auth.User']"}),
            'Meta': {'object_name': 'Event'},
            'creationTime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'eventCreator'", 'to': u"orm['auth.User']"}),
            'eventAddress': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'eventComputedEndTime': ('django.db.models.fields.DateTimeField', [], {}),
            'eventComputedStartTime': ('django.db.models.fields.DateTimeField', [], {}),
            'eventDescription': ('django.db.models.fields.CharField', [], {'max_length': '5000'}),
            'eventDuration': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'eventLocationDescription': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'eventName': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'eventStartTime': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'latitude': ('django.db.models.fields.FloatField', [], {}),
            'longitude': ('django.db.models.fields.FloatField', [], {}),
            'tasklist': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['event.Task']", 'symmetrical': 'False'})
        },
        u'event.frontline': {
            'Comments': ('django.db.models.fields.CharField', [], {'max_length': '50000'}),
            'Meta': {'object_name': 'Frontline'},
            'creationTime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'fname': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lname': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'organization': ('django.db.models.fields.CharField', [], {'max_length': '500'})
        },
        u'event.location': {
            'Meta': {'object_name': 'Location'},
            'creationTime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.FloatField', [], {}),
            'locationAddress': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'locationDescription': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'locationName': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'longitude': ('django.db.models.fields.FloatField', [], {}),
            'rsvps': ('django.db.models.fields.CharField', [], {'max_length': '500'})
        },
        u'event.profile': {
            'Meta': {'object_name': 'Profile'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True'})
        },
        u'event.task': {
            'Meta': {'object_name': 'Task'},
            'assignments': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.User']", 'symmetrical': 'False'}),
            'creationTime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'taskCreator'", 'to': u"orm['auth.User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'subtasks': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['event.Task']", 'symmetrical': 'False'}),
            'taskCompletiondate': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'taskDescription': ('django.db.models.fields.CharField', [], {'max_length': '5000'}),
            'taskDuedate': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'taskPriority': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'taskStatus': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'taskTitle': ('django.db.models.fields.CharField', [], {'max_length': '500'})
        },
        u'event.usercategory': {
            'Meta': {'object_name': 'Usercategory'},
            'group': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.Group']", 'unique': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.FileField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['event']