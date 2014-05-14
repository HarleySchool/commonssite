# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing unique constraint on 'ChannelNameMap', fields ['Panel', 'Channel']
        db.delete_unique('electic-channel-map', ['panel', 'channel'])

        # Deleting model 'ChannelNameMap'
        db.delete_table('electic-channel-map')

        # Renaming model 'ChannelEntry'
        db.rename_table('electric-channel', 'electric-circuits')

        # Adding model 'Panel'
        db.create_table(u'electric_panel', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('veris_id', self.gf('django.db.models.fields.IntegerField')()),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=16)),
        ))
        db.send_create_signal(u'electric', ['Panel'])

        # Adding model 'Circuit'
        db.create_table(u'electric_circuit', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('panel', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['electric.Panel'])),
            ('veris_id', self.gf('django.db.models.fields.IntegerField')()),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=32)),
        ))
        db.send_create_signal(u'electric', ['Circuit'])


    def backwards(self, orm):

        # Adding model 'ChannelNameMap'
        db.create_table('electic-channel-map', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('Name', self.gf('django.db.models.fields.CharField')(max_length=32, db_column='name')),
            ('Channel', self.gf('django.db.models.fields.CharField')(max_length=32, db_column='channel')),
            ('Panel', self.gf('django.db.models.fields.CharField')(max_length=16, db_column='panel')),
        ))
        db.send_create_signal(u'electric', ['ChannelNameMap'])

        # Adding unique constraint on 'ChannelNameMap', fields ['Panel', 'Channel']
        db.create_unique('electic-channel-map', ['panel', 'channel'])

        # Renaming model 'CircuitEntry'
        db.rename_table('electric-circuits', 'electric-channel')

        # Deleting model 'Panel'
        db.delete_table(u'electric_panel')

        # Deleting model 'Circuit'
        db.delete_table(u'electric_circuit')


    models = {
        u'electric.circuit': {
            'Meta': {'object_name': 'Circuit'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'panel': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['electric.Panel']"}),
            'veris_id': ('django.db.models.fields.IntegerField', [], {})
        },
        u'electric.circuitentry': {
            'Channel': ('django.db.models.fields.CharField', [], {'max_length': '32', 'db_column': "'channel'"}),
            'Current': ('django.db.models.fields.FloatField', [], {'db_column': "'current'"}),
            'Demand': ('django.db.models.fields.FloatField', [], {'db_column': "'demand'"}),
            'Energy': ('django.db.models.fields.FloatField', [], {'db_column': "'energy'"}),
            'MaxCurrent': ('django.db.models.fields.FloatField', [], {'db_column': "'current-max'"}),
            'MaxPower': ('django.db.models.fields.FloatField', [], {'db_column': "'power-max'"}),
            'Meta': {'unique_together': "(('Time', 'Channel', 'Panel'),)", 'object_name': 'CircuitEntry', 'db_table': "'electric-circuits'"},
            'Panel': ('django.db.models.fields.CharField', [], {'max_length': '16', 'db_column': "'panel'"}),
            'Power': ('django.db.models.fields.FloatField', [], {'db_column': "'power'"}),
            'PowerDemand': ('django.db.models.fields.FloatField', [], {'db_column': "'power-demand'"}),
            'PowerFactor': ('django.db.models.fields.FloatField', [], {'db_column': "'power-factor'"}),
            'Time': ('django.db.models.fields.DateTimeField', [], {'db_column': "'time'"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'temporary': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'electric.devicesummary': {
            'AToB': ('django.db.models.fields.FloatField', [], {'db_column': "'a_to_b'"}),
            'AToNeutral': ('django.db.models.fields.FloatField', [], {'db_column': "'a_to_neutral'"}),
            'AverageCurrent3Phase': ('django.db.models.fields.FloatField', [], {'db_column': "'avg_current'"}),
            'BToC': ('django.db.models.fields.FloatField', [], {'db_column': "'b_to_c'"}),
            'BToNeutral': ('django.db.models.fields.FloatField', [], {'db_column': "'b_to_neutral'"}),
            'CToA': ('django.db.models.fields.FloatField', [], {'db_column': "'c_to_a'"}),
            'CToNeutral': ('django.db.models.fields.FloatField', [], {'db_column': "'c_to_neutral'"}),
            'Demand': ('django.db.models.fields.FloatField', [], {'db_column': "'3ph_demand'"}),
            'Frequency': ('django.db.models.fields.FloatField', [], {'db_column': "'frequency'"}),
            'LineLine': ('django.db.models.fields.FloatField', [], {'db_column': "'line_line_3ph'"}),
            'LineNeutral': ('django.db.models.fields.FloatField', [], {'db_column': "'line_neutral_3ph'"}),
            'MaxDemand': ('django.db.models.fields.FloatField', [], {'db_column': "'max_3ph_demand'"}),
            'MaxPower': ('django.db.models.fields.FloatField', [], {'db_column': "'max_3ph_power'"}),
            'Meta': {'unique_together': "(('Time', 'Panel'),)", 'object_name': 'DeviceSummary', 'db_table': "'electric-summary'"},
            'Panel': ('django.db.models.fields.CharField', [], {'max_length': '16', 'db_column': "'panel'"}),
            'Phase1Current': ('django.db.models.fields.FloatField', [], {'db_column': "'phase_1_current'"}),
            'Phase1Demand': ('django.db.models.fields.FloatField', [], {'db_column': "'phase_1_demand'"}),
            'Phase1MaxCurrent': ('django.db.models.fields.FloatField', [], {'db_column': "'phase_1_max_current'"}),
            'Phase1MaxDemand': ('django.db.models.fields.FloatField', [], {'db_column': "'phase_1_max_demand'"}),
            'Phase1Power': ('django.db.models.fields.FloatField', [], {'db_column': "'phase_1_power'"}),
            'Phase1PowerFactor': ('django.db.models.fields.FloatField', [], {'db_column': "'phase_1_power_factor'"}),
            'Phase2Current': ('django.db.models.fields.FloatField', [], {'db_column': "'phase_2_current'"}),
            'Phase2Demand': ('django.db.models.fields.FloatField', [], {'db_column': "'phase_2_demand'"}),
            'Phase2MaxCurrent': ('django.db.models.fields.FloatField', [], {'db_column': "'phase_2_max_current'"}),
            'Phase2MaxDemand': ('django.db.models.fields.FloatField', [], {'db_column': "'phase_2_max_demand'"}),
            'Phase2Power': ('django.db.models.fields.FloatField', [], {'db_column': "'phase_2_power'"}),
            'Phase2PowerFactor': ('django.db.models.fields.FloatField', [], {'db_column': "'phase_2_power_factor'"}),
            'Phase3Current': ('django.db.models.fields.FloatField', [], {'db_column': "'phase_3_current'"}),
            'Phase3Demand': ('django.db.models.fields.FloatField', [], {'db_column': "'phase_3_demand'"}),
            'Phase3MaxCurrent': ('django.db.models.fields.FloatField', [], {'db_column': "'phase_3_max_current'"}),
            'Phase3MaxDemand': ('django.db.models.fields.FloatField', [], {'db_column': "'phase_3_max_demand'"}),
            'Phase3Power': ('django.db.models.fields.FloatField', [], {'db_column': "'phase_3_power'"}),
            'Phase3PowerFactor': ('django.db.models.fields.FloatField', [], {'db_column': "'phase_3_power_factor'"}),
            'PhaseNeutralCurrent': ('django.db.models.fields.FloatField', [], {'db_column': "'phase_neutral_current'"}),
            'PhaseNeutralDemand': ('django.db.models.fields.FloatField', [], {'db_column': "'phase_neutral_demand'"}),
            'PhaseNeutralMaxCurrent': ('django.db.models.fields.FloatField', [], {'db_column': "'phase_neutral_max_current'"}),
            'PhaseNeutralMaxDemand': ('django.db.models.fields.FloatField', [], {'db_column': "'phase_neutral_max_demand'"}),
            'Time': ('django.db.models.fields.DateTimeField', [], {'db_column': "'time'"}),
            'TotalEnergy': ('django.db.models.fields.FloatField', [], {'db_column': "'total_energy'"}),
            'TotalPower': ('django.db.models.fields.FloatField', [], {'db_column': "'total_power'"}),
            'TotalPowerFactor': ('django.db.models.fields.FloatField', [], {'db_column': "'total_power_factor'"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'temporary': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'electric.panel': {
            'Meta': {'object_name': 'Panel'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'veris_id': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['electric']