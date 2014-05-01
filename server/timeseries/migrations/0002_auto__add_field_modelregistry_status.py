# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'ModelRegistry.status'
        db.add_column(u'timeseries_modelregistry', 'status',
                      self.gf('django.db.models.fields.IntegerField')(default=2),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'ModelRegistry.status'
        db.delete_column(u'timeseries_modelregistry', 'status')


    models = {
        u'timeseries.modelregistry': {
            'Meta': {'object_name': 'ModelRegistry'},
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model_class': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'scraper_class': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True'}),
            'short_name': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'status': ('django.db.models.fields.IntegerField', [], {}),
            'system': ('django.db.models.fields.CharField', [], {'max_length': '16'})
        }
    }

    complete_apps = ['timeseries']