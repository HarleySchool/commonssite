# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'CircuitEntry.temporary'
        db.add_column('electric-channel', 'temporary',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'DeviceSummary.temporary'
        db.add_column('electric-summary', 'temporary',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'CircuitEntry.temporary'
        db.delete_column('electric-channel', 'temporary')

        # Deleting field 'DeviceSummary.temporary'
        db.delete_column('electric-summary', 'temporary')


    models = {
        u'electric.channelentry': {
            'Channel': ('django.db.models.fields.CharField', [], {'max_length': '32', 'db_column': "'channel'"}),
            'Current': ('django.db.models.fields.FloatField', [], {'db_column': "'current'"}),
            'Demand': ('django.db.models.fields.FloatField', [], {'db_column': "'demand'"}),
            'Energy': ('django.db.models.fields.FloatField', [], {'db_column': "'energy'"}),
            'MaxCurrent': ('django.db.models.fields.FloatField', [], {'db_column': "'current-max'"}),
            'MaxPower': ('django.db.models.fields.FloatField', [], {'db_column': "'power-max'"}),
            'Meta': {'unique_together': "(('Time', 'Channel', 'Panel'),)", 'object_name': 'CircuitEntry', 'db_table': "'electric-channel'"},
            'Panel': ('django.db.models.fields.CharField', [], {'max_length': '16', 'db_column': "'panel'"}),
            'Power': ('django.db.models.fields.FloatField', [], {'db_column': "'power'"}),
            'PowerDemand': ('django.db.models.fields.FloatField', [], {'db_column': "'power-demand'"}),
            'PowerFactor': ('django.db.models.fields.FloatField', [], {'db_column': "'power-factor'"}),
            'Time': ('django.db.models.fields.DateTimeField', [], {'db_column': "'time'"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'temporary': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'electric.channelnamemap': {
            'Channel': ('django.db.models.fields.CharField', [], {'max_length': '32', 'db_column': "'channel'"}),
            'Meta': {'unique_together': "(('Panel', 'Channel'),)", 'object_name': 'ChannelNameMap', 'db_table': "'electic-channel-map'"},
            'Name': ('django.db.models.fields.CharField', [], {'max_length': '32', 'db_column': "'name'"}),
            'Panel': ('django.db.models.fields.CharField', [], {'max_length': '16', 'db_column': "'panel'"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
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
        }
    }

    complete_apps = ['electric']