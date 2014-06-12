# -*- coding: utf-8 -*-
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):

        # Renaming field 'ErvEntry.Name'
        db.rename_column('hvac-erv', 'NameIndex_id', 'name')
        # Renaming field 'ErvEntry.AirDirection'
        db.rename_column('hvac-erv', 'AirDirectionIndex_id', 'air direction')
        # Renaming field 'ErvEntry.FanSpeed'
        db.rename_column('hvac-erv', 'FanSpeedIndex_id', 'fan speed')
        # Renaming field 'ErvEntry.Mode'
        db.rename_column('hvac-erv', 'ModeIndex_id', 'mode')
        # Adding unique constraint on 'ErvEntry', fields ['Time', 'Name']
        db.create_unique('hvac-erv', ['time', 'name'])

        # Renaming field 'VrfEntry.Name'
        db.rename_column('hvac-vrf', 'NameIndex_id', 'name')
        # Renaming field 'VrfEntry.AirDirection'
        db.rename_column('hvac-vrf', 'AirDirectionIndex_id', 'air direction')
        # Renaming field 'VrfEntry.FanSpeed'
        db.rename_column('hvac-vrf', 'FanSpeedIndex_id', 'fan speed')
        # Renaming field 'VrfEntry.Mode'
        db.rename_column('hvac-vrf', 'ModeIndex_id', 'mode')
        # Adding unique constraint on 'VrfEntry', fields ['Time', 'Name']
        db.create_unique('hvac-vrf', ['time', 'name'])


    def backwards(self, orm):
        # Removing unique constraint on 'VrfEntry', fields ['Time', 'Name']
        db.delete_unique('hvac-vrf', ['time', 'name'])
        # Removing unique constraint on 'ErvEntry', fields ['Time', 'Name']
        db.delete_unique('hvac-erv', ['time', 'name'])

        # Renaming field 'ErvEntry.Name'
        db.rename_column('hvac-erv', 'name', 'NameIndex_id')
        # Renaming field 'ErvEntry.AirDirection'
        db.rename_column('hvac-erv', 'air direction', 'AirDirectionIndex_id')
        # Renaming field 'ErvEntry.FanSpeed'
        db.rename_column('hvac-erv', 'fan speed', 'FanSpeedIndex_id')
        # Renaming field 'ErvEntry.Mode'
        db.rename_column('hvac-erv', 'mode', 'ModeIndex_id')

        # Renaming field 'VrfEntry.Name'
        db.rename_column('hvac-vrf', 'name', 'NameIndex_id')
        # Renaming field 'VrfEntry.AirDirection'
        db.rename_column('hvac-vrf', 'air direction', 'AirDirectionIndex_id')
        # Renaming field 'VrfEntry.FanSpeed'
        db.rename_column('hvac-vrf', 'fan speed', 'FanSpeedIndex_id')
        # Renaming field 'VrfEntry.Mode'
        db.rename_column('hvac-vrf', 'mode', 'ModeIndex_id')


    models = {
        u'hvac.erventry': {
            'AirDirection': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': u"orm['hvac.FanDirections']", 'db_column': "'air direction'"}),
            'ErrorSign': ('django.db.models.fields.BooleanField', [], {'db_column': "'error'"}),
            'FanSpeed': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': u"orm['hvac.FanSpeeds']", 'db_column': "'fan speed'"}),
            'InletTemp': ('django.db.models.fields.FloatField', [], {'db_column': "'measured temp'"}),
            'Meta': {'unique_together': "(('Time', 'Name'),)", 'object_name': 'ErvEntry', 'db_table': "'hvac-erv'"},
            'Mode': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': u"orm['hvac.Modes']", 'db_column': "'mode'"}),
            'Name': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': u"orm['hvac.Rooms']", 'db_column': "'name'"}),
            'Running': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'db_column': "'running'", 'blank': 'True'}),
            'Time': ('django.db.models.fields.DateTimeField', [], {'db_column': "'time'"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'temporary': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'hvac.fandirections': {
            'Meta': {'object_name': 'FanDirections'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '14'})
        },
        u'hvac.fanspeeds': {
            'Meta': {'object_name': 'FanSpeeds'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '8'})
        },
        u'hvac.modes': {
            'Meta': {'object_name': 'Modes'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '12'})
        },
        u'hvac.rooms': {
            'Meta': {'object_name': 'Rooms'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '32'})
        },
        u'hvac.vrfentry': {
            'AirDirection': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': u"orm['hvac.FanDirections']", 'db_column': "'air direction'"}),
            'AutoMax': ('django.db.models.fields.FloatField', [], {'db_column': "'auto max'"}),
            'AutoMin': ('django.db.models.fields.FloatField', [], {'db_column': "'auto min'"}),
            'CoolMax': ('django.db.models.fields.FloatField', [], {'db_column': "'cool max'"}),
            'CoolMin': ('django.db.models.fields.FloatField', [], {'db_column': "'cool min'"}),
            'ErrorSign': ('django.db.models.fields.BooleanField', [], {'db_column': "'error'"}),
            'FanSpeed': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': u"orm['hvac.FanSpeeds']", 'db_column': "'fan speed'"}),
            'HeatMax': ('django.db.models.fields.FloatField', [], {'db_column': "'heat max'"}),
            'HeatMin': ('django.db.models.fields.FloatField', [], {'db_column': "'heat min'"}),
            'InletTemp': ('django.db.models.fields.FloatField', [], {'db_column': "'measured temp'"}),
            'Meta': {'unique_together': "(('Time', 'Name'),)", 'object_name': 'VrfEntry', 'db_table': "'hvac-vrf'"},
            'Mode': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': u"orm['hvac.Modes']", 'db_column': "'mode'"}),
            'Name': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': u"orm['hvac.Rooms']", 'db_column': "'name'"}),
            'Running': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'db_column': "'running'", 'blank': 'True'}),
            'SetTemp': ('django.db.models.fields.FloatField', [], {'db_column': "'set temp'"}),
            'Time': ('django.db.models.fields.DateTimeField', [], {'db_column': "'time'"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'temporary': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        }
    }

    complete_apps = ['hvac']