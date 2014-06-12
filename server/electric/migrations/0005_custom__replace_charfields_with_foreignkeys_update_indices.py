# -*- coding: utf-8 -*-
from south.db import db
from south.v2 import SchemaMigration

class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing unique constraint on 'CircuitEntry', fields ['Time', 'Channel', 'Panel']
        # (to be replaced by ['Time', 'Circuit'])
        db.delete_unique('electric-circuits', ['time', 'channel', 'panel'])
        # Deleting field 'CircuitEntry.Channel'
        db.delete_column('electric-circuits', 'channel')
        # Deleting field 'CircuitEntry.Panel'
        db.delete_column('electric-circuits', 'panel')
        # Renaming column for 'CircuitEntry.Circuit'
        db.rename_column('electric-circuits', 'circuit', 'circuit_id')
        # Create index for use in uniqe constraint
        db.create_index('electric-circuits', ['circuit_id'])
        # Adding unique constraint on 'CircuitEntry', fields ['Time', 'Circuit']
        db.create_unique('electric-circuits', ['time', 'circuit_id'])

        # Remove unique on 'DeviceSummary', fields ['time', 'panel']
        db.delete_unique('electric-summary', ['time', 'panel'])
        # Adding index on 'DeviceSummary', fields ['Panel']
        db.create_index('electric-summary', ['panel_id'])
        # create unique constraint using panel_id
        db.create_unique('electric-summary', ['time', 'panel_id'])
        # remove old panel field
        db.delete_column('electric-summary', 'panel')


    def backwards(self, orm):
        # TODO sql queries inside migrations so that they can actually be used
        print "CAN'T ACTUALLY MIGRATE BACKWARDS FROM 0005 SAFELY. YOU SHOULD QUIT NOW."
        raw_input()
        """# Removing unique constraint on 'CircuitEntry', fields ['Time', 'Circuit']
                                db.delete_unique('electric-circuits', ['time', 'circuit_id'])
                                # Removing index on 'CircuitEntry', fields ['Circuit']
                                db.delete_index('electric-circuits', ['circuit_id'])
                                # Renaming column for 'CircuitEntry.Circuit' to match new field type.
                                db.rename_column('electric-circuits', 'circuit_id', 'circuit')
                                # Adding field 'CircuitEntry.Channel'
                                db.add_column('electric-circuits', 'Channel',
                                              self.gf('django.db.models.fields.CharField')(default='Channel XX', max_length=32, db_column='channel'),
                                              keep_default=False)
                                # Adding field 'CircuitEntry.Panel'
                                db.add_column('electric-circuits', 'Panel',
                                              self.gf('django.db.models.fields.CharField')(default='Panel XX', max_length=16, db_column='panel'),
                                              keep_default=False)
                                # Adding unique constraint on 'CircuitEntry', fields ['Time', 'Channel', 'Panel']
                                db.create_unique('electric-circuits', ['time', 'channel', 'panel'])
                        
                                # add old 'panel' column back in
                                db.add_column('electric-summary', 'Panel',
                                              self.gf('django.db.models.fields.CharField')(default='Panel XX', max_length=16, db_column='panel'),
                                              keep_default=False)
                                db.delete_unique('electric-summary', ['time', 'panel_id'])
                                db.delete_index('electric-summary', ['panel_id'])
                                db.create_unique('electric-summary', ['time', 'panel'])"""


    models = {
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