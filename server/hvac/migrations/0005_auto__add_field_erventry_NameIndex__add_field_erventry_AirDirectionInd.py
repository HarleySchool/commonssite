# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'ErvEntry.NameIndex'
        db.add_column('hvac-erv', 'NameIndex',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['hvac.Rooms']),
                      keep_default=False)

        # Adding field 'ErvEntry.AirDirectionIndex'
        db.add_column('hvac-erv', 'AirDirectionIndex',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['hvac.FanDirections']),
                      keep_default=False)

        # Adding field 'ErvEntry.FanSpeedIndex'
        db.add_column('hvac-erv', 'FanSpeedIndex',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['hvac.FanSpeeds']),
                      keep_default=False)

        # Adding field 'ErvEntry.ModeIndex'
        db.add_column('hvac-erv', 'ModeIndex',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['hvac.Modes']),
                      keep_default=False)

        # Adding field 'VrfEntry.NameIndex'
        db.add_column('hvac-vrf', 'NameIndex',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['hvac.Rooms']),
                      keep_default=False)

        # Adding field 'VrfEntry.AirDirectionIndex'
        db.add_column('hvac-vrf', 'AirDirectionIndex',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['hvac.FanDirections']),
                      keep_default=False)

        # Adding field 'VrfEntry.FanSpeedIndex'
        db.add_column('hvac-vrf', 'FanSpeedIndex',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['hvac.FanSpeeds']),
                      keep_default=False)

        # Adding field 'VrfEntry.ModeIndex'
        db.add_column('hvac-vrf', 'ModeIndex',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['hvac.Modes']),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'ErvEntry.NameIndex'
        db.delete_column('hvac-erv', 'NameIndex_id')

        # Deleting field 'ErvEntry.AirDirectionIndex'
        db.delete_column('hvac-erv', 'AirDirectionIndex_id')

        # Deleting field 'ErvEntry.FanSpeedIndex'
        db.delete_column('hvac-erv', 'FanSpeedIndex_id')

        # Deleting field 'ErvEntry.ModeIndex'
        db.delete_column('hvac-erv', 'ModeIndex_id')

        # Deleting field 'VrfEntry.NameIndex'
        db.delete_column('hvac-vrf', 'NameIndex_id')

        # Deleting field 'VrfEntry.AirDirectionIndex'
        db.delete_column('hvac-vrf', 'AirDirectionIndex_id')

        # Deleting field 'VrfEntry.FanSpeedIndex'
        db.delete_column('hvac-vrf', 'FanSpeedIndex_id')

        # Deleting field 'VrfEntry.ModeIndex'
        db.delete_column('hvac-vrf', 'ModeIndex_id')


    models = {
        u'hvac.erventry': {
            'AirDirection': ('django.db.models.fields.CharField', [], {'max_length': '16', 'db_column': "'air direction'"}),
            'AirDirectionIndex': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': u"orm['hvac.FanDirections']"}),
            'ErrorSign': ('django.db.models.fields.BooleanField', [], {'db_column': "'error'"}),
            'FanSpeed': ('django.db.models.fields.CharField', [], {'max_length': '8', 'db_column': "'fan speed'"}),
            'FanSpeedIndex': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': u"orm['hvac.FanSpeeds']"}),
            'InletTemp': ('django.db.models.fields.FloatField', [], {'db_column': "'measured temp'"}),
            'Meta': {'unique_together': "(('Time', 'Name'),)", 'object_name': 'ErvEntry', 'db_table': "'hvac-erv'"},
            'Mode': ('django.db.models.fields.CharField', [], {'max_length': '14', 'db_column': "'mode'"}),
            'ModeIndex': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': u"orm['hvac.Modes']"}),
            'Name': ('django.db.models.fields.CharField', [], {'max_length': '32', 'db_column': "'name'"}),
            'NameIndex': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': u"orm['hvac.Rooms']"}),
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
            'AirDirection': ('django.db.models.fields.CharField', [], {'max_length': '16', 'db_column': "'air direction'"}),
            'AirDirectionIndex': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': u"orm['hvac.FanDirections']"}),
            'AutoMax': ('django.db.models.fields.FloatField', [], {'db_column': "'auto max'"}),
            'AutoMin': ('django.db.models.fields.FloatField', [], {'db_column': "'auto min'"}),
            'CoolMax': ('django.db.models.fields.FloatField', [], {'db_column': "'cool max'"}),
            'CoolMin': ('django.db.models.fields.FloatField', [], {'db_column': "'cool min'"}),
            'ErrorSign': ('django.db.models.fields.BooleanField', [], {'db_column': "'error'"}),
            'FanSpeed': ('django.db.models.fields.CharField', [], {'max_length': '8', 'db_column': "'fan speed'"}),
            'FanSpeedIndex': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': u"orm['hvac.FanSpeeds']"}),
            'HeatMax': ('django.db.models.fields.FloatField', [], {'db_column': "'heat max'"}),
            'HeatMin': ('django.db.models.fields.FloatField', [], {'db_column': "'heat min'"}),
            'InletTemp': ('django.db.models.fields.FloatField', [], {'db_column': "'measured temp'"}),
            'Meta': {'unique_together': "(('Time', 'Name'),)", 'object_name': 'VrfEntry', 'db_table': "'hvac-vrf'"},
            'Mode': ('django.db.models.fields.CharField', [], {'max_length': '14', 'db_column': "'mode'"}),
            'ModeIndex': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': u"orm['hvac.Modes']"}),
            'Name': ('django.db.models.fields.CharField', [], {'max_length': '32', 'db_column': "'name'"}),
            'NameIndex': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': u"orm['hvac.Rooms']"}),
            'Running': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'db_column': "'running'", 'blank': 'True'}),
            'SetTemp': ('django.db.models.fields.FloatField', [], {'db_column': "'set temp'"}),
            'Time': ('django.db.models.fields.DateTimeField', [], {'db_column': "'time'"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'temporary': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        }
    }

    complete_apps = ['hvac']