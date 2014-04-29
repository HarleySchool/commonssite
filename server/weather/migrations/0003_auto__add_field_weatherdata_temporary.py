# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'WeatherData.temporary'
        db.add_column(u'weather_weatherdata', 'temporary',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'WeatherData.temporary'
        db.delete_column(u'weather_weatherdata', 'temporary')


    models = {
        u'weather.weatherdata': {
            'Meta': {'object_name': 'WeatherData'},
            'Time': ('django.db.models.fields.DateTimeField', [], {'db_column': "'time'"}),
            'barometer': ('django.db.models.fields.FloatField', [], {}),
            'dayet': ('django.db.models.fields.FloatField', [], {}),
            'dayrain': ('django.db.models.fields.FloatField', [], {}),
            'dewpoint': ('django.db.models.fields.FloatField', [], {}),
            'heatindex': ('django.db.models.fields.FloatField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inhumidity': ('django.db.models.fields.FloatField', [], {}),
            'intemp': ('django.db.models.fields.FloatField', [], {}),
            'monthet': ('django.db.models.fields.FloatField', [], {}),
            'monthrain': ('django.db.models.fields.FloatField', [], {}),
            'outhumidity': ('django.db.models.fields.FloatField', [], {}),
            'outtemp': ('django.db.models.fields.FloatField', [], {}),
            'radiation': ('django.db.models.fields.FloatField', [], {}),
            'rain': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'rainrate': ('django.db.models.fields.FloatField', [], {}),
            'stormrain': ('django.db.models.fields.FloatField', [], {}),
            'stormstart': ('django.db.models.fields.FloatField', [], {}),
            'sunrise': ('django.db.models.fields.FloatField', [], {}),
            'sunset': ('django.db.models.fields.FloatField', [], {}),
            'temporary': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'uv': ('django.db.models.fields.FloatField', [], {}),
            'windchill': ('django.db.models.fields.FloatField', [], {}),
            'winddir': ('django.db.models.fields.FloatField', [], {}),
            'windspeed': ('django.db.models.fields.FloatField', [], {}),
            'yearet': ('django.db.models.fields.FloatField', [], {}),
            'yearrain': ('django.db.models.fields.FloatField', [], {})
        }
    }

    complete_apps = ['weather']