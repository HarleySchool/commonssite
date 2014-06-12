# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'SMAWeather.AmbientTemprature'
        db.delete_column('sma-weather', 'AmbientTemprature')

        # Deleting field 'SMAWeather.InternalSolarIrradation'
        db.delete_column('sma-weather', 'InternalSolarIrradation')

        # Deleting field 'SMAOverview.Message'
        db.delete_column('sma-overview', 'Message')

        # Deleting field 'SMAPanels.DeviceControlStatus'
        db.delete_column('sma-panels', 'DeviceControlStatus')

        # Deleting field 'SMAPanels.OperationHealth'
        db.delete_column('sma-panels', 'OperationHealth')

        # Deleting field 'SMAPanels.OperatingTime'
        db.delete_column('sma-panels', 'OperatingTime')

        # Deleting field 'SMAPanels.TotalYield'
        db.delete_column('sma-panels', 'TotalYield')

        # Deleting field 'SMAPanels.Derating'
        db.delete_column('sma-panels', 'Derating')


    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'SMAWeather.AmbientTemprature'
        raise RuntimeError("Cannot reverse this migration. 'SMAWeather.AmbientTemprature' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'SMAWeather.AmbientTemprature'
        db.add_column('sma-weather', 'AmbientTemprature',
                      self.gf('django.db.models.fields.FloatField')(),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'SMAWeather.InternalSolarIrradation'
        raise RuntimeError("Cannot reverse this migration. 'SMAWeather.InternalSolarIrradation' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'SMAWeather.InternalSolarIrradation'
        db.add_column('sma-weather', 'InternalSolarIrradation',
                      self.gf('django.db.models.fields.FloatField')(),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'SMAOverview.Message'
        raise RuntimeError("Cannot reverse this migration. 'SMAOverview.Message' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'SMAOverview.Message'
        db.add_column('sma-overview', 'Message',
                      self.gf('django.db.models.fields.CharField')(max_length=128),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'SMAPanels.DeviceControlStatus'
        raise RuntimeError("Cannot reverse this migration. 'SMAPanels.DeviceControlStatus' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'SMAPanels.DeviceControlStatus'
        db.add_column('sma-panels', 'DeviceControlStatus',
                      self.gf('django.db.models.fields.CharField')(max_length=8),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'SMAPanels.OperationHealth'
        raise RuntimeError("Cannot reverse this migration. 'SMAPanels.OperationHealth' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'SMAPanels.OperationHealth'
        db.add_column('sma-panels', 'OperationHealth',
                      self.gf('django.db.models.fields.CharField')(max_length=16),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'SMAPanels.OperatingTime'
        raise RuntimeError("Cannot reverse this migration. 'SMAPanels.OperatingTime' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'SMAPanels.OperatingTime'
        db.add_column('sma-panels', 'OperatingTime',
                      self.gf('django.db.models.fields.FloatField')(),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'SMAPanels.TotalYield'
        raise RuntimeError("Cannot reverse this migration. 'SMAPanels.TotalYield' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'SMAPanels.TotalYield'
        db.add_column('sma-panels', 'TotalYield',
                      self.gf('django.db.models.fields.FloatField')(),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'SMAPanels.Derating'
        raise RuntimeError("Cannot reverse this migration. 'SMAPanels.Derating' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'SMAPanels.Derating'
        db.add_column('sma-panels', 'Derating',
                      self.gf('django.db.models.fields.CharField')(max_length=10),
                      keep_default=False)


    models = {
        u'solar.smaoverview': {
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
            'ResidualCurrent': ('django.db.models.fields.FloatField', [], {}),
            'Time': ('django.db.models.fields.DateTimeField', [], {'db_column': "'time'"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'temporary': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'solar.smaweather': {
            'ExternalSolarIrradation': ('django.db.models.fields.FloatField', [], {}),
            'Meta': {'object_name': 'SMAWeather', 'db_table': "'sma-weather'"},
            'ModuleTemprature': ('django.db.models.fields.FloatField', [], {}),
            'Time': ('django.db.models.fields.DateTimeField', [], {'db_column': "'time'"}),
            'WindVelocity': ('django.db.models.fields.FloatField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'temporary': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        }
    }

    complete_apps = ['solar']