# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ErvEntry'
        db.create_table('hvac-erv', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('Time', self.gf('django.db.models.fields.DateTimeField')(db_column='time')),
            ('Name', self.gf('django.db.models.fields.CharField')(max_length=32, db_column='name')),
            ('AirDirection', self.gf('django.db.models.fields.CharField')(max_length=12, db_column='air direction')),
            ('FanSpeed', self.gf('django.db.models.fields.CharField')(max_length=8, db_column='fan speed')),
            ('Mode', self.gf('django.db.models.fields.CharField')(max_length=14, db_column='mode')),
            ('ErrorSign', self.gf('django.db.models.fields.BooleanField')(db_column='error')),
            ('InletTemp', self.gf('django.db.models.fields.FloatField')(db_column='measured temp')),
        ))
        db.send_create_signal('data', ['ErvEntry'])

        # Adding unique constraint on 'ErvEntry', fields ['Time', 'Name']
        db.create_unique('hvac-erv', ['time', 'name'])

        # Adding model 'VrfEntry'
        db.create_table('hvac-vrf', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('Time', self.gf('django.db.models.fields.DateTimeField')(db_column='time')),
            ('Name', self.gf('django.db.models.fields.CharField')(max_length=32, db_column='name')),
            ('AirDirection', self.gf('django.db.models.fields.CharField')(max_length=12, db_column='air direction')),
            ('FanSpeed', self.gf('django.db.models.fields.CharField')(max_length=8, db_column='fan speed')),
            ('Mode', self.gf('django.db.models.fields.CharField')(max_length=14, db_column='mode')),
            ('ErrorSign', self.gf('django.db.models.fields.BooleanField')(db_column='error')),
            ('InletTemp', self.gf('django.db.models.fields.FloatField')(db_column='measured temp')),
            ('HeatMax', self.gf('django.db.models.fields.FloatField')(db_column='heat max')),
            ('HeatMin', self.gf('django.db.models.fields.FloatField')(db_column='heat min')),
            ('CoolMax', self.gf('django.db.models.fields.FloatField')(db_column='cool max')),
            ('CoolMin', self.gf('django.db.models.fields.FloatField')(db_column='cool min')),
            ('AutoMax', self.gf('django.db.models.fields.FloatField')(db_column='auto max')),
            ('AutoMin', self.gf('django.db.models.fields.FloatField')(db_column='auto min')),
            ('SetTemp', self.gf('django.db.models.fields.FloatField')(db_column='set temp')),
        ))
        db.send_create_signal('data', ['VrfEntry'])

        # Adding unique constraint on 'VrfEntry', fields ['Time', 'Name']
        db.create_unique('hvac-vrf', ['time', 'name'])


    def backwards(self, orm):
        # Removing unique constraint on 'VrfEntry', fields ['Time', 'Name']
        db.delete_unique('hvac-vrf', ['time', 'name'])

        # Removing unique constraint on 'ErvEntry', fields ['Time', 'Name']
        db.delete_unique('hvac-erv', ['time', 'name'])

        # Deleting model 'ErvEntry'
        db.delete_table('hvac-erv')

        # Deleting model 'VrfEntry'
        db.delete_table('hvac-vrf')


    models = {
        'data.erventry': {
            'AirDirection': ('django.db.models.fields.CharField', [], {'max_length': '12', 'db_column': "'air direction'"}),
            'ErrorSign': ('django.db.models.fields.BooleanField', [], {'db_column': "'error'"}),
            'FanSpeed': ('django.db.models.fields.CharField', [], {'max_length': '8', 'db_column': "'fan speed'"}),
            'InletTemp': ('django.db.models.fields.FloatField', [], {'db_column': "'measured temp'"}),
            'Meta': {'unique_together': "(('Time', 'Name'),)", 'object_name': 'ErvEntry', 'db_table': "'hvac-erv'"},
            'Mode': ('django.db.models.fields.CharField', [], {'max_length': '14', 'db_column': "'mode'"}),
            'Name': ('django.db.models.fields.CharField', [], {'max_length': '32', 'db_column': "'name'"}),
            'Time': ('django.db.models.fields.DateTimeField', [], {'db_column': "'time'"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'data.vrfentry': {
            'AirDirection': ('django.db.models.fields.CharField', [], {'max_length': '12', 'db_column': "'air direction'"}),
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
            'SetTemp': ('django.db.models.fields.FloatField', [], {'db_column': "'set temp'"}),
            'Time': ('django.db.models.fields.DateTimeField', [], {'db_column': "'time'"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['data']