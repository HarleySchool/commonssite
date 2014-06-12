# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Series'
        db.create_table(u'timeseries_series', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('spec', self.gf('jsonfield.fields.JSONField')(default={})),
            ('string_hash', self.gf('django.db.models.fields.CharField')(max_length=24)),
        ))
        db.send_create_signal(u'timeseries', ['Series'])


    def backwards(self, orm):
        # Deleting model 'Series'
        db.delete_table(u'timeseries_series')


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
        },
        u'timeseries.series': {
            'Meta': {'object_name': 'Series'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'spec': ('jsonfield.fields.JSONField', [], {'default': '{}'}),
            'string_hash': ('django.db.models.fields.CharField', [], {'max_length': '24'})
        }
    }

    complete_apps = ['timeseries']