# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'CalculatedStats'
        db.create_table(u'electric_calculatedstats', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('Time', self.gf('django.db.models.fields.DateTimeField')(db_column='time')),
            ('temporary', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('GrossPowerUsed', self.gf('django.db.models.fields.FloatField')(null=True)),
            ('GrossPowerFactorUsed', self.gf('django.db.models.fields.FloatField')(null=True)),
            ('GrossEnergyUsed', self.gf('django.db.models.fields.FloatField')(null=True)),
            ('GrossPowerProduced', self.gf('django.db.models.fields.FloatField')(null=True)),
            ('GrossPowerFactorProduced', self.gf('django.db.models.fields.FloatField')(null=True)),
            ('GrossEnergyProduced', self.gf('django.db.models.fields.FloatField')(null=True)),
            ('NetPower', self.gf('django.db.models.fields.FloatField')(null=True)),
            ('NetPowerFactor', self.gf('django.db.models.fields.FloatField')(null=True)),
            ('NetEnergy', self.gf('django.db.models.fields.FloatField')(null=True)),
        ))
        db.send_create_signal(u'electric', ['CalculatedStats'])


    def backwards(self, orm):
        # Deleting model 'CalculatedStats'
        db.delete_table(u'electric_calculatedstats')


    models = {
        u'electric.calculatedstats': {
            'GrossEnergyProduced': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'GrossEnergyUsed': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'GrossPowerFactorProduced': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'GrossPowerFactorUsed': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'GrossPowerProduced': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'GrossPowerUsed': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'Meta': {'object_name': 'CalculatedStats'},
            'NetEnergy': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'NetPower': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'NetPowerFactor': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'Time': ('django.db.models.fields.DateTimeField', [], {'db_column': "'time'"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'temporary': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'electric.circuit': {
            'Meta': {'object_name': 'Circuit'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'panel': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['electric.Panel']"}),
            'veris_id': ('django.db.models.fields.IntegerField', [], {})
        },
        u'electric.circuitentry': {
            'Circuit': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': u"orm['electric.Circuit']", 'db_column': "'circuit_id'"}),
            'Current': ('django.db.models.fields.FloatField', [], {'db_column': "'current'"}),
            'Demand': ('django.db.models.fields.FloatField', [], {'db_column': "'demand'"}),
            'Energy': ('django.db.models.fields.FloatField', [], {'db_column': "'energy'"}),
            'MaxCurrent': ('django.db.models.fields.FloatField', [], {'db_column': "'current-max'"}),
            'MaxPower': ('django.db.models.fields.FloatField', [], {'db_column': "'power-max'"}),
            'Meta': {'unique_together': "(('Time', 'Circuit'),)", 'object_name': 'CircuitEntry', 'db_table': "'electric-circuits'"},
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
            'Panel': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': u"orm['electric.Panel']", 'db_column': "'panel_id'"}),
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