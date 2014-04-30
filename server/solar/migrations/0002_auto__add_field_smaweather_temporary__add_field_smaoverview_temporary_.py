# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'SMAWeather.temporary'
        db.add_column('sma-weather', 'temporary',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'SMAOverview.temporary'
        db.add_column('sma-overview', 'temporary',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'SMAPanels.temporary'
        db.add_column('sma-panels', 'temporary',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'SMAWeather.temporary'
        db.delete_column('sma-weather', 'temporary')

        # Deleting field 'SMAOverview.temporary'
        db.delete_column('sma-overview', 'temporary')

        # Deleting field 'SMAPanels.temporary'
        db.delete_column('sma-panels', 'temporary')


    models = {
        u'solar.smaoverview': {
            'Message': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'Meta': {'object_name': 'SMAOverview', 'db_table': "'sma-overview'"},
            'Time': ('django.db.models.fields.DateTimeField', [], {'db_column': "'time'"}),
            'TotalACPower': ('django.db.models.fields.FloatField', [], {}),
            'TotalEnergy': ('django.db.models.fields.FloatField', [], {}),
            'TotalEnergyToday': ('django.db.models.fields.FloatField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'temporary': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'solar.smapanels': {
            'A1_DC_Current': ('django.db.models.fields.FloatField', [], {}),
            'A_DC_Current': ('django.db.models.fields.FloatField', [], {}),
            'A_DC_Power': ('django.db.models.fields.FloatField', [], {}),
            'A_DC_Voltage': ('django.db.models.fields.FloatField', [], {}),
            'B1_DC_Current': ('django.db.models.fields.FloatField', [], {}),
            'B_DC_Current': ('django.db.models.fields.FloatField', [], {}),
            'B_DC_Power': ('django.db.models.fields.FloatField', [], {}),
            'B_DC_Voltage': ('django.db.models.fields.FloatField', [], {}),
            'Derating': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'DeviceControlStatus': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'FeedInTime': ('django.db.models.fields.FloatField', [], {}),
            'GridApparentPower': ('django.db.models.fields.FloatField', [], {}),
            'GridDisplacementPowerFactor': ('django.db.models.fields.FloatField', [], {}),
            'GridFrequency': ('django.db.models.fields.FloatField', [], {}),
            'GridPhase1ApparentPower': ('django.db.models.fields.FloatField', [], {}),
            'GridPhase1Current': ('django.db.models.fields.FloatField', [], {}),
            'GridPhase1Power': ('django.db.models.fields.FloatField', [], {}),
            'GridPhase1ReactivePower': ('django.db.models.fields.FloatField', [], {}),
            'GridPhase1Voltage': ('django.db.models.fields.FloatField', [], {}),
            'GridPhase2ApparentPower': ('django.db.models.fields.FloatField', [], {}),
            'GridPhase2Current': ('django.db.models.fields.FloatField', [], {}),
            'GridPhase2Power': ('django.db.models.fields.FloatField', [], {}),
            'GridPhase2ReactivePower': ('django.db.models.fields.FloatField', [], {}),
            'GridPhase2Voltage': ('django.db.models.fields.FloatField', [], {}),
            'GridPhase3ApparentPower': ('django.db.models.fields.FloatField', [], {}),
            'GridPhase3Current': ('django.db.models.fields.FloatField', [], {}),
            'GridPhase3Power': ('django.db.models.fields.FloatField', [], {}),
            'GridPhase3ReactivePower': ('django.db.models.fields.FloatField', [], {}),
            'GridPhase3Voltage': ('django.db.models.fields.FloatField', [], {}),
            'GridReactivePower': ('django.db.models.fields.FloatField', [], {}),
            'Meta': {'object_name': 'SMAPanels', 'db_table': "'sma-panels'"},
            'OperatingTime': ('django.db.models.fields.FloatField', [], {}),
            'OperationHealth': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'ResidualCurrent': ('django.db.models.fields.FloatField', [], {}),
            'Time': ('django.db.models.fields.DateTimeField', [], {'db_column': "'time'"}),
            'TotalYield': ('django.db.models.fields.FloatField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'temporary': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'solar.smaweather': {
            'AmbientTemprature': ('django.db.models.fields.FloatField', [], {}),
            'ExternalSolarIrradation': ('django.db.models.fields.FloatField', [], {}),
            'InternalSolarIrradation': ('django.db.models.fields.FloatField', [], {}),
            'Meta': {'object_name': 'SMAWeather', 'db_table': "'sma-weather'"},
            'ModuleTemprature': ('django.db.models.fields.FloatField', [], {}),
            'Time': ('django.db.models.fields.DateTimeField', [], {'db_column': "'time'"}),
            'WindVelocity': ('django.db.models.fields.FloatField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'temporary': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        }
    }

    complete_apps = ['solar']