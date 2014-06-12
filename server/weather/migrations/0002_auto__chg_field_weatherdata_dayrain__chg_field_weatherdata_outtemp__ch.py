# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'WeatherData.dayrain'
        db.alter_column(u'weather_weatherdata', 'dayrain', self.gf('django.db.models.fields.FloatField')(default=0))

        # Changing field 'WeatherData.outtemp'
        db.alter_column(u'weather_weatherdata', 'outtemp', self.gf('django.db.models.fields.FloatField')(default=0))

        # Changing field 'WeatherData.intemp'
        db.alter_column(u'weather_weatherdata', 'intemp', self.gf('django.db.models.fields.FloatField')(default=0))

        # Changing field 'WeatherData.yearrain'
        db.alter_column(u'weather_weatherdata', 'yearrain', self.gf('django.db.models.fields.FloatField')(default=0))

        # Changing field 'WeatherData.sunrise'
        db.alter_column(u'weather_weatherdata', 'sunrise', self.gf('django.db.models.fields.FloatField')(default=0))

        # Changing field 'WeatherData.yearet'
        db.alter_column(u'weather_weatherdata', 'yearet', self.gf('django.db.models.fields.FloatField')(default=0))

        # Changing field 'WeatherData.outhumidity'
        db.alter_column(u'weather_weatherdata', 'outhumidity', self.gf('django.db.models.fields.FloatField')(default=0))

        # Changing field 'WeatherData.heatindex'
        db.alter_column(u'weather_weatherdata', 'heatindex', self.gf('django.db.models.fields.FloatField')(default=0))

        # Changing field 'WeatherData.radiation'
        db.alter_column(u'weather_weatherdata', 'radiation', self.gf('django.db.models.fields.FloatField')(default=0))

        # Changing field 'WeatherData.monthrain'
        db.alter_column(u'weather_weatherdata', 'monthrain', self.gf('django.db.models.fields.FloatField')(default=0))

        # Changing field 'WeatherData.stormrain'
        db.alter_column(u'weather_weatherdata', 'stormrain', self.gf('django.db.models.fields.FloatField')(default=0))

        # Changing field 'WeatherData.monthet'
        db.alter_column(u'weather_weatherdata', 'monthet', self.gf('django.db.models.fields.FloatField')(default=0))

        # Changing field 'WeatherData.barometer'
        db.alter_column(u'weather_weatherdata', 'barometer', self.gf('django.db.models.fields.FloatField')(default=0))

        # Changing field 'WeatherData.windchill'
        db.alter_column(u'weather_weatherdata', 'windchill', self.gf('django.db.models.fields.FloatField')(default=0))

        # Changing field 'WeatherData.dewpoint'
        db.alter_column(u'weather_weatherdata', 'dewpoint', self.gf('django.db.models.fields.FloatField')(default=0))

        # Changing field 'WeatherData.dayet'
        db.alter_column(u'weather_weatherdata', 'dayet', self.gf('django.db.models.fields.FloatField')(default=0))

        # Changing field 'WeatherData.winddir'
        db.alter_column(u'weather_weatherdata', 'winddir', self.gf('django.db.models.fields.FloatField')(default=0))

        # Changing field 'WeatherData.windspeed'
        db.alter_column(u'weather_weatherdata', 'windspeed', self.gf('django.db.models.fields.FloatField')(default=0))

        # Changing field 'WeatherData.stormstart'
        db.alter_column(u'weather_weatherdata', 'stormstart', self.gf('django.db.models.fields.FloatField')(default=0))

        # Changing field 'WeatherData.inhumidity'
        db.alter_column(u'weather_weatherdata', 'inhumidity', self.gf('django.db.models.fields.FloatField')(default=0))

        # Changing field 'WeatherData.uv'
        db.alter_column(u'weather_weatherdata', 'uv', self.gf('django.db.models.fields.FloatField')(default=0))

        # Changing field 'WeatherData.sunset'
        db.alter_column(u'weather_weatherdata', 'sunset', self.gf('django.db.models.fields.FloatField')(default=0))

        # Changing field 'WeatherData.rainrate'
        db.alter_column(u'weather_weatherdata', 'rainrate', self.gf('django.db.models.fields.FloatField')(default=0))

    def backwards(self, orm):

        # Changing field 'WeatherData.dayrain'
        db.alter_column(u'weather_weatherdata', 'dayrain', self.gf('django.db.models.fields.FloatField')(null=True))

        # Changing field 'WeatherData.outtemp'
        db.alter_column(u'weather_weatherdata', 'outtemp', self.gf('django.db.models.fields.FloatField')(null=True))

        # Changing field 'WeatherData.intemp'
        db.alter_column(u'weather_weatherdata', 'intemp', self.gf('django.db.models.fields.FloatField')(null=True))

        # Changing field 'WeatherData.yearrain'
        db.alter_column(u'weather_weatherdata', 'yearrain', self.gf('django.db.models.fields.FloatField')(null=True))

        # Changing field 'WeatherData.sunrise'
        db.alter_column(u'weather_weatherdata', 'sunrise', self.gf('django.db.models.fields.FloatField')(null=True))

        # Changing field 'WeatherData.yearet'
        db.alter_column(u'weather_weatherdata', 'yearet', self.gf('django.db.models.fields.FloatField')(null=True))

        # Changing field 'WeatherData.outhumidity'
        db.alter_column(u'weather_weatherdata', 'outhumidity', self.gf('django.db.models.fields.FloatField')(null=True))

        # Changing field 'WeatherData.heatindex'
        db.alter_column(u'weather_weatherdata', 'heatindex', self.gf('django.db.models.fields.FloatField')(null=True))

        # Changing field 'WeatherData.radiation'
        db.alter_column(u'weather_weatherdata', 'radiation', self.gf('django.db.models.fields.FloatField')(null=True))

        # Changing field 'WeatherData.monthrain'
        db.alter_column(u'weather_weatherdata', 'monthrain', self.gf('django.db.models.fields.FloatField')(null=True))

        # Changing field 'WeatherData.stormrain'
        db.alter_column(u'weather_weatherdata', 'stormrain', self.gf('django.db.models.fields.FloatField')(null=True))

        # Changing field 'WeatherData.monthet'
        db.alter_column(u'weather_weatherdata', 'monthet', self.gf('django.db.models.fields.FloatField')(null=True))

        # Changing field 'WeatherData.barometer'
        db.alter_column(u'weather_weatherdata', 'barometer', self.gf('django.db.models.fields.FloatField')(null=True))

        # Changing field 'WeatherData.windchill'
        db.alter_column(u'weather_weatherdata', 'windchill', self.gf('django.db.models.fields.FloatField')(null=True))

        # Changing field 'WeatherData.dewpoint'
        db.alter_column(u'weather_weatherdata', 'dewpoint', self.gf('django.db.models.fields.FloatField')(null=True))

        # Changing field 'WeatherData.dayet'
        db.alter_column(u'weather_weatherdata', 'dayet', self.gf('django.db.models.fields.FloatField')(null=True))

        # Changing field 'WeatherData.winddir'
        db.alter_column(u'weather_weatherdata', 'winddir', self.gf('django.db.models.fields.FloatField')(null=True))

        # Changing field 'WeatherData.windspeed'
        db.alter_column(u'weather_weatherdata', 'windspeed', self.gf('django.db.models.fields.FloatField')(null=True))

        # Changing field 'WeatherData.stormstart'
        db.alter_column(u'weather_weatherdata', 'stormstart', self.gf('django.db.models.fields.FloatField')(null=True))

        # Changing field 'WeatherData.inhumidity'
        db.alter_column(u'weather_weatherdata', 'inhumidity', self.gf('django.db.models.fields.FloatField')(null=True))

        # Changing field 'WeatherData.uv'
        db.alter_column(u'weather_weatherdata', 'uv', self.gf('django.db.models.fields.FloatField')(null=True))

        # Changing field 'WeatherData.sunset'
        db.alter_column(u'weather_weatherdata', 'sunset', self.gf('django.db.models.fields.FloatField')(null=True))

        # Changing field 'WeatherData.rainrate'
        db.alter_column(u'weather_weatherdata', 'rainrate', self.gf('django.db.models.fields.FloatField')(null=True))

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
            'uv': ('django.db.models.fields.FloatField', [], {}),
            'windchill': ('django.db.models.fields.FloatField', [], {}),
            'winddir': ('django.db.models.fields.FloatField', [], {}),
            'windspeed': ('django.db.models.fields.FloatField', [], {}),
            'yearet': ('django.db.models.fields.FloatField', [], {}),
            'yearrain': ('django.db.models.fields.FloatField', [], {})
        }
    }

    complete_apps = ['weather']