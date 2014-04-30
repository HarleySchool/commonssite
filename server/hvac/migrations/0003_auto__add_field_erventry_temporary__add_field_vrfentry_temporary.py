# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'ErvEntry.temporary'
        db.add_column('hvac-erv', 'temporary',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'VrfEntry.temporary'
        db.add_column('hvac-vrf', 'temporary',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'ErvEntry.temporary'
        db.delete_column('hvac-erv', 'temporary')

        # Deleting field 'VrfEntry.temporary'
        db.delete_column('hvac-vrf', 'temporary')


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