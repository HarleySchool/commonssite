# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'WeatherData'
        db.create_table(u'weather_weatherdata', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('Time', self.gf('django.db.models.fields.DateTimeField')(db_column='time')),
            ('uv', self.gf('django.db.models.fields.FloatField')(null=True)),
            ('barometer', self.gf('django.db.models.fields.FloatField')(null=True)),
            ('dayet', self.gf('django.db.models.fields.FloatField')(null=True)),
            ('dayrain', self.gf('django.db.models.fields.FloatField')(null=True)),
            ('dewpoint', self.gf('django.db.models.fields.FloatField')(null=True)),
            ('heatindex', self.gf('django.db.models.fields.FloatField')(null=True)),
            ('inhumidity', self.gf('django.db.models.fields.FloatField')(null=True)),
            ('intemp', self.gf('django.db.models.fields.FloatField')(null=True)),
            ('monthet', self.gf('django.db.models.fields.FloatField')(null=True)),
            ('monthrain', self.gf('django.db.models.fields.FloatField')(null=True)),
            ('outhumidity', self.gf('django.db.models.fields.FloatField')(null=True)),
            ('outtemp', self.gf('django.db.models.fields.FloatField')(null=True)),
            ('radiation', self.gf('django.db.models.fields.FloatField')(null=True)),
            ('rain', self.gf('django.db.models.fields.FloatField')(null=True)),
            ('rainrate', self.gf('django.db.models.fields.FloatField')(null=True)),
            ('stormrain', self.gf('django.db.models.fields.FloatField')(null=True)),
            ('stormstart', self.gf('django.db.models.fields.FloatField')(null=True)),
            ('sunrise', self.gf('django.db.models.fields.FloatField')(null=True)),
            ('sunset', self.gf('django.db.models.fields.FloatField')(null=True)),
            ('winddir', self.gf('django.db.models.fields.FloatField')(null=True)),
            ('windspeed', self.gf('django.db.models.fields.FloatField')(null=True)),
            ('windchill', self.gf('django.db.models.fields.FloatField')(null=True)),
            ('yearet', self.gf('django.db.models.fields.FloatField')(null=True)),
            ('yearrain', self.gf('django.db.models.fields.FloatField')(null=True)),
        ))
        db.send_create_signal(u'weather', ['WeatherData'])


    def backwards(self, orm):
        # Deleting model 'WeatherData'
        db.delete_table(u'weather_weatherdata')


    models = {
        u'weather.weatherdata': {
            'Meta': {'object_name': 'WeatherData'},
            'Time': ('django.db.models.fields.DateTimeField', [], {'db_column': "'time'"}),
            'barometer': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'dayet': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'dayrain': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'dewpoint': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'heatindex': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inhumidity': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'intemp': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'monthet': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'monthrain': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'outhumidity': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'outtemp': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'radiation': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'rain': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'rainrate': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'stormrain': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'stormstart': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'sunrise': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'sunset': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'uv': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'windchill': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'winddir': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'windspeed': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'yearet': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'yearrain': ('django.db.models.fields.FloatField', [], {'null': 'True'})
        }
    }

    complete_apps = ['weather']