# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ChannelNameMap'
        db.create_table('electic-channel-map', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('Panel', self.gf('django.db.models.fields.CharField')(max_length=16, db_column='panel')),
            ('Channel', self.gf('django.db.models.fields.CharField')(max_length=32, db_column='channel')),
            ('Name', self.gf('django.db.models.fields.CharField')(max_length=32, db_column='name')),
        ))
        db.send_create_signal(u'electric', ['ChannelNameMap'])

        # Adding unique constraint on 'ChannelNameMap', fields ['Panel', 'Channel']
        db.create_unique('electic-channel-map', ['panel', 'channel'])

        # Adding model 'CircuitEntry'
        db.create_table('electric-channel', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('Time', self.gf('django.db.models.fields.DateTimeField')(db_column='time')),
            ('Panel', self.gf('django.db.models.fields.CharField')(max_length=16, db_column='panel')),
            ('Channel', self.gf('django.db.models.fields.CharField')(max_length=32, db_column='channel')),
            ('Current', self.gf('django.db.models.fields.FloatField')(db_column='current')),
            ('Energy', self.gf('django.db.models.fields.FloatField')(db_column='energy')),
            ('MaxCurrent', self.gf('django.db.models.fields.FloatField')(db_column='current-max')),
            ('Demand', self.gf('django.db.models.fields.FloatField')(db_column='demand')),
            ('Power', self.gf('django.db.models.fields.FloatField')(db_column='power')),
            ('MaxPower', self.gf('django.db.models.fields.FloatField')(db_column='power-max')),
            ('PowerDemand', self.gf('django.db.models.fields.FloatField')(db_column='power-demand')),
            ('PowerFactor', self.gf('django.db.models.fields.FloatField')(db_column='power-factor')),
        ))
        db.send_create_signal(u'electric', ['CircuitEntry'])

        # Adding unique constraint on 'CircuitEntry', fields ['Time', 'Channel', 'Panel']
        db.create_unique('electric-channel', ['time', 'channel', 'panel'])

        # Adding model 'DeviceSummary'
        db.create_table('electric-summary', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('Time', self.gf('django.db.models.fields.DateTimeField')(db_column='time')),
            ('Panel', self.gf('django.db.models.fields.CharField')(max_length=16, db_column='panel')),
            ('Frequency', self.gf('django.db.models.fields.FloatField')(db_column='frequency')),
            ('LineNeutral', self.gf('django.db.models.fields.FloatField')(db_column='line_neutral_3ph')),
            ('LineLine', self.gf('django.db.models.fields.FloatField')(db_column='line_line_3ph')),
            ('AToNeutral', self.gf('django.db.models.fields.FloatField')(db_column='a_to_neutral')),
            ('BToNeutral', self.gf('django.db.models.fields.FloatField')(db_column='b_to_neutral')),
            ('CToNeutral', self.gf('django.db.models.fields.FloatField')(db_column='c_to_neutral')),
            ('AToB', self.gf('django.db.models.fields.FloatField')(db_column='a_to_b')),
            ('BToC', self.gf('django.db.models.fields.FloatField')(db_column='b_to_c')),
            ('CToA', self.gf('django.db.models.fields.FloatField')(db_column='c_to_a')),
            ('TotalEnergy', self.gf('django.db.models.fields.FloatField')(db_column='total_energy')),
            ('TotalPower', self.gf('django.db.models.fields.FloatField')(db_column='total_power')),
            ('TotalPowerFactor', self.gf('django.db.models.fields.FloatField')(db_column='total_power_factor')),
            ('AverageCurrent3Phase', self.gf('django.db.models.fields.FloatField')(db_column='avg_current')),
            ('Phase1Power', self.gf('django.db.models.fields.FloatField')(db_column='phase_1_power')),
            ('Phase2Power', self.gf('django.db.models.fields.FloatField')(db_column='phase_2_power')),
            ('Phase3Power', self.gf('django.db.models.fields.FloatField')(db_column='phase_3_power')),
            ('Phase1PowerFactor', self.gf('django.db.models.fields.FloatField')(db_column='phase_1_power_factor')),
            ('Phase2PowerFactor', self.gf('django.db.models.fields.FloatField')(db_column='phase_2_power_factor')),
            ('Phase3PowerFactor', self.gf('django.db.models.fields.FloatField')(db_column='phase_3_power_factor')),
            ('Phase1Current', self.gf('django.db.models.fields.FloatField')(db_column='phase_1_current')),
            ('Phase2Current', self.gf('django.db.models.fields.FloatField')(db_column='phase_2_current')),
            ('Phase3Current', self.gf('django.db.models.fields.FloatField')(db_column='phase_3_current')),
            ('PhaseNeutralCurrent', self.gf('django.db.models.fields.FloatField')(db_column='phase_neutral_current')),
            ('Phase1Demand', self.gf('django.db.models.fields.FloatField')(db_column='phase_1_demand')),
            ('Phase2Demand', self.gf('django.db.models.fields.FloatField')(db_column='phase_2_demand')),
            ('Phase3Demand', self.gf('django.db.models.fields.FloatField')(db_column='phase_3_demand')),
            ('PhaseNeutralDemand', self.gf('django.db.models.fields.FloatField')(db_column='phase_neutral_demand')),
            ('Phase1MaxDemand', self.gf('django.db.models.fields.FloatField')(db_column='phase_1_max_demand')),
            ('Phase2MaxDemand', self.gf('django.db.models.fields.FloatField')(db_column='phase_2_max_demand')),
            ('Phase3MaxDemand', self.gf('django.db.models.fields.FloatField')(db_column='phase_3_max_demand')),
            ('PhaseNeutralMaxDemand', self.gf('django.db.models.fields.FloatField')(db_column='phase_neutral_max_demand')),
            ('Demand', self.gf('django.db.models.fields.FloatField')(db_column='3ph_demand')),
            ('MaxDemand', self.gf('django.db.models.fields.FloatField')(db_column='max_3ph_demand')),
            ('Phase1MaxCurrent', self.gf('django.db.models.fields.FloatField')(db_column='phase_1_max_current')),
            ('Phase2MaxCurrent', self.gf('django.db.models.fields.FloatField')(db_column='phase_2_max_current')),
            ('Phase3MaxCurrent', self.gf('django.db.models.fields.FloatField')(db_column='phase_3_max_current')),
            ('PhaseNeutralMaxCurrent', self.gf('django.db.models.fields.FloatField')(db_column='phase_neutral_max_current')),
            ('MaxPower', self.gf('django.db.models.fields.FloatField')(db_column='max_3ph_power')),
        ))
        db.send_create_signal(u'electric', ['DeviceSummary'])

        # Adding unique constraint on 'DeviceSummary', fields ['Time', 'Panel']
        db.create_unique('electric-summary', ['time', 'panel'])


    def backwards(self, orm):
        # Removing unique constraint on 'DeviceSummary', fields ['Time', 'Panel']
        db.delete_unique('electric-summary', ['time', 'panel'])

        # Removing unique constraint on 'CircuitEntry', fields ['Time', 'Channel', 'Panel']
        db.delete_unique('electric-channel', ['time', 'channel', 'panel'])

        # Removing unique constraint on 'ChannelNameMap', fields ['Panel', 'Channel']
        db.delete_unique('electic-channel-map', ['panel', 'channel'])

        # Deleting model 'ChannelNameMap'
        db.delete_table('electic-channel-map')

        # Deleting model 'CircuitEntry'
        db.delete_table('electric-channel')

        # Deleting model 'DeviceSummary'
        db.delete_table('electric-summary')


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
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
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
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['electric']