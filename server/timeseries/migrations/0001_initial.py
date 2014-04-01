# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ModelRegistry'
        db.create_table(u'timeseries_modelregistry', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('system', self.gf('django.db.models.fields.CharField')(max_length=16)),
            ('model_class', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('scraper_class', self.gf('django.db.models.fields.CharField')(max_length=64, null=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('short_name', self.gf('django.db.models.fields.CharField')(max_length=32)),
        ))
        db.send_create_signal(u'timeseries', ['ModelRegistry'])


    def backwards(self, orm):
        # Deleting model 'ModelRegistry'
        db.delete_table(u'timeseries_modelregistry')


    models = {
        u'timeseries.modelregistry': {
            'Meta': {'object_name': 'ModelRegistry'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model_class': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'scraper_class': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True'}),
            'short_name': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'system': ('django.db.models.fields.CharField', [], {'max_length': '16'})
        }
    }

    complete_apps = ['timeseries']