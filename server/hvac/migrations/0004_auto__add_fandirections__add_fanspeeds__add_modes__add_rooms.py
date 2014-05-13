# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'FanDirections'
        db.create_table(u'hvac_fandirections', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=14)),
        ))
        db.send_create_signal(u'hvac', ['FanDirections'])

        # Adding model 'FanSpeeds'
        db.create_table(u'hvac_fanspeeds', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=8)),
        ))
        db.send_create_signal(u'hvac', ['FanSpeeds'])

        # Adding model 'Modes'
        db.create_table(u'hvac_modes', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=12)),
        ))
        db.send_create_signal(u'hvac', ['Modes'])

        # Adding model 'Rooms'
        db.create_table(u'hvac_rooms', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=32)),
        ))
        db.send_create_signal(u'hvac', ['Rooms'])


    def backwards(self, orm):
        # Deleting model 'FanDirections'
        db.delete_table(u'hvac_fandirections')

        # Deleting model 'FanSpeeds'
        db.delete_table(u'hvac_fanspeeds')

        # Deleting model 'Modes'
        db.delete_table(u'hvac_modes')

        # Deleting model 'Rooms'
        db.delete_table(u'hvac_rooms')


    models = {
        u'hvac.erventry': {
            'AirDirection': ('django.db.models.fields.CharField', [], {'max_length': '16', 'db_column': "'air direction'"}),
            'ErrorSign': ('django.db.models.fields.BooleanField', [], {'db_column': "'error'"}),
            'FanSpeed': ('django.db.models.fields.CharField', [], {'max_length': '8', 'db_column': "'fan speed'"}),
            'InletTemp': ('django.db.models.fields.FloatField', [], {'db_column': "'measured temp'"}),
            'Meta': {'unique_together': "(('Time', 'Name'),)", 'object_name': 'ErvEntry', 'db_table': "'hvac-erv'"},
            'Mode': ('django.db.models.fields.CharField', [], {'max_length': '14', 'db_column': "'mode'"}),
            'Name': ('django.db.models.fields.CharField', [], {'max_length': '32', 'db_column': "'name'"}),
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
            'AutoMax': ('django.db.models.fields.FloatField', [], {'db_column': "'auto max'"}),
            'AutoMin': ('django.db.models.fields.FloatField', [], {'db_column': "'auto min'"}),
            'CoolMax': ('django.db.models.fields.FloatField', [], {'db_column': "'cool max'"}),
            'CoolMin': ('django.db.models.fields.FloatField', [], {'db_column': "'cool min'"}),
            'ErrorSign': ('django.db.models.fields.BooleanField', [], {'db_column': "'error'"}),
            'FanSpeed': ('django.db.models.fields.CharField', [], {'max_length': '8', 'db_column': "'fan speed'"}),
            'HeatMax': ('django.db.models.fields.FloatField', [], {'db_column': "'heat max'"}),
            'HeatMin': ('django.db.models.fields.FloatField', [], {'db_column': "'heat min'"}),
            'InletTemp': ('django.db.models.fields.FloatField', [], {'db_column': "'measured temp'"}),
            'Meta': {'unique_together': "(('Time', 'Name'),)", 'object_name': 'VrfEntry', 'db_table': "'hvac-vrf'"},
            'Mode': ('django.db.models.fields.CharField', [], {'max_length': '14', 'db_column': "'mode'"}),
            'Name': ('django.db.models.fields.CharField', [], {'max_length': '32', 'db_column': "'name'"}),
            'Running': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'db_column': "'running'", 'blank': 'True'}),
            'SetTemp': ('django.db.models.fields.FloatField', [], {'db_column': "'set temp'"}),
            'Time': ('django.db.models.fields.DateTimeField', [], {'db_column': "'time'"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'temporary': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        }
    }

    complete_apps = ['hvac']