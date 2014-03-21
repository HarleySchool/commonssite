# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'SMAWeather'
        db.create_table('sma-weather', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('Time', self.gf('django.db.models.fields.DateTimeField')(db_column='time')),
            ('InternalSolarIrradation', self.gf('django.db.models.fields.FloatField')()),
            ('ExternalSolarIrradation', self.gf('django.db.models.fields.FloatField')()),
            ('AmbientTemprature', self.gf('django.db.models.fields.FloatField')()),
            ('ModuleTemprature', self.gf('django.db.models.fields.FloatField')()),
            ('WindVelocity', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal(u'solar', ['SMAWeather'])

        # Adding model 'SMAOverview'
        db.create_table('sma-overview', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('Time', self.gf('django.db.models.fields.DateTimeField')(db_column='time')),
            ('TotalACPower', self.gf('django.db.models.fields.FloatField')()),
            ('TotalEnergyToday', self.gf('django.db.models.fields.FloatField')()),
            ('TotalEnergy', self.gf('django.db.models.fields.FloatField')()),
            ('Message', self.gf('django.db.models.fields.CharField')(max_length=128)),
        ))
        db.send_create_signal(u'solar', ['SMAOverview'])

        # Adding model 'SMAPanels'
        db.create_table('sma-panels', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('Time', self.gf('django.db.models.fields.DateTimeField')(db_column='time')),
            ('A_DC_Current', self.gf('django.db.models.fields.FloatField')()),
            ('A_DC_Voltage', self.gf('django.db.models.fields.FloatField')()),
            ('A_DC_Power', self.gf('django.db.models.fields.FloatField')()),
            ('A1_DC_Current', self.gf('django.db.models.fields.FloatField')()),
            ('B_DC_Current', self.gf('django.db.models.fields.FloatField')()),
            ('B_DC_Voltage', self.gf('django.db.models.fields.FloatField')()),
            ('B_DC_Power', self.gf('django.db.models.fields.FloatField')()),
            ('B1_DC_Current', self.gf('django.db.models.fields.FloatField')()),
            ('TotalYield', self.gf('django.db.models.fields.FloatField')()),
            ('GridPhase1Current', self.gf('django.db.models.fields.FloatField')()),
            ('GridPhase2Current', self.gf('django.db.models.fields.FloatField')()),
            ('GridPhase3Current', self.gf('django.db.models.fields.FloatField')()),
            ('GridFrequency', self.gf('django.db.models.fields.FloatField')()),
            ('GridPhase1Voltage', self.gf('django.db.models.fields.FloatField')()),
            ('GridPhase2Voltage', self.gf('django.db.models.fields.FloatField')()),
            ('GridPhase3Voltage', self.gf('django.db.models.fields.FloatField')()),
            ('GridDisplacementPowerFactor', self.gf('django.db.models.fields.FloatField')()),
            ('GridApparentPower', self.gf('django.db.models.fields.FloatField')()),
            ('GridReactivePower', self.gf('django.db.models.fields.FloatField')()),
            ('GridPhase1ApparentPower', self.gf('django.db.models.fields.FloatField')()),
            ('GridPhase2ApparentPower', self.gf('django.db.models.fields.FloatField')()),
            ('GridPhase3ApparentPower', self.gf('django.db.models.fields.FloatField')()),
            ('GridPhase1ReactivePower', self.gf('django.db.models.fields.FloatField')()),
            ('GridPhase2ReactivePower', self.gf('django.db.models.fields.FloatField')()),
            ('GridPhase3ReactivePower', self.gf('django.db.models.fields.FloatField')()),
            ('GridPhase1Power', self.gf('django.db.models.fields.FloatField')()),
            ('GridPhase2Power', self.gf('django.db.models.fields.FloatField')()),
            ('GridPhase3Power', self.gf('django.db.models.fields.FloatField')()),
            ('Derating', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('DeviceControlStatus', self.gf('django.db.models.fields.CharField')(max_length=8)),
            ('ResidualCurrent', self.gf('django.db.models.fields.FloatField')()),
            ('FeedInTime', self.gf('django.db.models.fields.FloatField')()),
            ('OperatingTime', self.gf('django.db.models.fields.FloatField')()),
            ('OperationHealth', self.gf('django.db.models.fields.CharField')(max_length=16)),
            ('TotalACPower', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal(u'solar', ['SMAPanels'])


    def backwards(self, orm):
        # Deleting model 'SMAWeather'
        db.delete_table('sma-weather')

        # Deleting model 'SMAOverview'
        db.delete_table('sma-overview')

        # Deleting model 'SMAPanels'
        db.delete_table('sma-panels')


    models = {
        u'solar.smaoverview': {
            'Message': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'Meta': {'object_name': 'SMAOverview', 'db_table': "'sma-overview'"},
            'Time': ('django.db.models.fields.DateTimeField', [], {'db_column': "'time'"}),
            'TotalACPower': ('django.db.models.fields.FloatField', [], {}),
            'TotalEnergy': ('django.db.models.fields.FloatField', [], {}),
            'TotalEnergyToday': ('django.db.models.fields.FloatField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
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
            'TotalACPower': ('django.db.models.fields.FloatField', [], {}),
            'TotalYield': ('django.db.models.fields.FloatField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'solar.smaweather': {
            'AmbientTemprature': ('django.db.models.fields.FloatField', [], {}),
            'ExternalSolarIrradation': ('django.db.models.fields.FloatField', [], {}),
            'InternalSolarIrradation': ('django.db.models.fields.FloatField', [], {}),
            'Meta': {'object_name': 'SMAWeather', 'db_table': "'sma-weather'"},
            'ModuleTemprature': ('django.db.models.fields.FloatField', [], {}),
            'Time': ('django.db.models.fields.DateTimeField', [], {'db_column': "'time'"}),
            'WindVelocity': ('django.db.models.fields.FloatField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['solar']