# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Live.rowspan'
        db.delete_column(u'timeseries_live', 'rowspan')


    def backwards(self, orm):
        # Adding field 'Live.rowspan'
        db.add_column(u'timeseries_live', 'rowspan',
                      self.gf('django.db.models.fields.IntegerField')(default=1),
                      keep_default=False)


    models = {
        u'timeseries.live': {
            'Meta': {'object_name': 'Live'},
            'colspan': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.IntegerField', [], {}),
            'series': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['timeseries.Series']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '40'})
        },
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