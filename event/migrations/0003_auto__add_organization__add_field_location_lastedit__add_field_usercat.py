# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Organization'
        db.create_table(u'event_organization', (
            (u'usercategory_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['event.Usercategory'], unique=True, primary_key=True)),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
        ))
        db.send_create_signal(u'event', ['Organization'])

        # Adding M2M table for field Admins on 'Organization'
        m2m_table_name = db.shorten_name(u'event_organization_Admins')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('organization', models.ForeignKey(orm[u'event.organization'], null=False)),
            ('user', models.ForeignKey(orm[u'auth.user'], null=False))
        ))
        db.create_unique(m2m_table_name, ['organization_id', 'user_id'])

        # Adding field 'Location.lastedit'
        db.add_column(u'event_location', 'lastedit',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='LocationLastedit', null=True, to=orm['auth.User']),
                      keep_default=False)

        # Adding field 'Usercategory.lastedit'
        db.add_column(u'event_usercategory', 'lastedit',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='categoryLastedit', null=True, to=orm['auth.User']),
                      keep_default=False)

        # Adding field 'Event.lastedit'
        db.add_column(u'event_event', 'lastedit',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='eventLastedit', null=True, to=orm['auth.User']),
                      keep_default=False)

        # Adding field 'Event.Organization'
        db.add_column(u'event_event', 'Organization',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['event.Organization'], null=True, blank=True),
                      keep_default=False)

        # Adding M2M table for field EventCheckins on 'Event'
        m2m_table_name = db.shorten_name(u'event_event_EventCheckins')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('event', models.ForeignKey(orm[u'event.event'], null=False)),
            ('user', models.ForeignKey(orm[u'auth.user'], null=False))
        ))
        db.create_unique(m2m_table_name, ['event_id', 'user_id'])

        # Adding field 'Task.lastedit'
        db.add_column(u'event_task', 'lastedit',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='taskLastedit', null=True, to=orm['auth.User']),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting model 'Organization'
        db.delete_table(u'event_organization')

        # Removing M2M table for field Admins on 'Organization'
        db.delete_table(db.shorten_name(u'event_organization_Admins'))

        # Deleting field 'Location.lastedit'
        db.delete_column(u'event_location', 'lastedit_id')

        # Deleting field 'Usercategory.lastedit'
        db.delete_column(u'event_usercategory', 'lastedit_id')

        # Deleting field 'Event.lastedit'
        db.delete_column(u'event_event', 'lastedit_id')

        # Deleting field 'Event.Organization'
        db.delete_column(u'event_event', 'Organization_id')

        # Removing M2M table for field EventCheckins on 'Event'
        db.delete_table(db.shorten_name(u'event_event_EventCheckins'))

        # Deleting field 'Task.lastedit'
        db.delete_column(u'event_task', 'lastedit_id')


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
            'EventCheckins': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'eventCheckins'", 'blank': 'True', 'to': u"orm['auth.User']"}),
            'EventRSVPS': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'eventrsvplist'", 'blank': 'True', 'to': u"orm['auth.User']"}),
            'Meta': {'object_name': 'Event'},
            'Organization': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['event.Organization']", 'null': 'True', 'blank': 'True'}),
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
            'lastedit': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'eventLastedit'", 'null': 'True', 'to': u"orm['auth.User']"}),
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
            'lastedit': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'LocationLastedit'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'latitude': ('django.db.models.fields.FloatField', [], {}),
            'locationAddress': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'locationDescription': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'locationName': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'longitude': ('django.db.models.fields.FloatField', [], {}),
            'rsvps': ('django.db.models.fields.CharField', [], {'max_length': '500'})
        },
        u'event.organization': {
            'Admins': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'OrgAdmin'", 'blank': 'True', 'to': u"orm['auth.User']"}),
            'Meta': {'object_name': 'Organization', '_ormbases': [u'event.Usercategory']},
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            u'usercategory_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['event.Usercategory']", 'unique': 'True', 'primary_key': 'True'})
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
            'lastedit': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'taskLastedit'", 'null': 'True', 'to': u"orm['auth.User']"}),
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
            'description': ('django.db.models.fields.CharField', [], {'default': "' '", 'max_length': '50000'}),
            'group': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.Group']", 'unique': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'lastedit': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'categoryLastedit'", 'null': 'True', 'to': u"orm['auth.User']"})
        }
    }

    complete_apps = ['event']