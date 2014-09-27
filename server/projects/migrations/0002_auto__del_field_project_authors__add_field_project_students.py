# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Project.authors'
        db.delete_column(u'projects_project', 'authors')

        # Adding field 'Project.students'
        db.add_column(u'projects_project', 'students',
                      self.gf('django.db.models.fields.CharField')(default=None, max_length=256),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'Project.authors'
        db.add_column(u'projects_project', 'authors',
                      self.gf('django.db.models.fields.CharField')(default=None, max_length=256),
                      keep_default=False)

        # Deleting field 'Project.students'
        db.delete_column(u'projects_project', 'students')


    models = {
        u'projects.project': {
            'Meta': {'object_name': 'Project'},
            'classroom': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'content': ('django.db.models.fields.TextField', [], {}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'students': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        }
    }

    complete_apps = ['projects']