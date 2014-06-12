# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing unique constraint on 'VrfEntry', fields ['Time', 'Name']
        db.delete_unique('hvac-vrf', ['time', 'name'])

        # Removing unique constraint on 'ErvEntry', fields ['Time', 'Name']
        db.delete_unique('hvac-erv', ['time', 'name'])

        # Deleting field 'ErvEntry.Name'
        db.delete_column('hvac-erv', 'name')

        # Deleting field 'ErvEntry.FanSpeed'
        db.delete_column('hvac-erv', 'fan speed')

        # Deleting field 'ErvEntry.Mode'
        db.delete_column('hvac-erv', 'mode')

        # Deleting field 'ErvEntry.AirDirection'
        db.delete_column('hvac-erv', 'air direction')

        # Deleting field 'VrfEntry.Name'
        db.delete_column('hvac-vrf', 'name')

        # Deleting field 'VrfEntry.FanSpeed'
        db.delete_column('hvac-vrf', 'fan speed')

        # Deleting field 'VrfEntry.Mode'
        db.delete_column('hvac-vrf', 'mode')

        # Deleting field 'VrfEntry.AirDirection'
        db.delete_column('hvac-vrf', 'air direction')


    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'ErvEntry.Name'
        raise RuntimeError("Cannot reverse this migration. 'ErvEntry.Name' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'ErvEntry.Name'
        db.add_column('hvac-erv', 'Name',
                      self.gf('django.db.models.fields.CharField')(max_length=32, db_column='name'),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'ErvEntry.FanSpeed'
        raise RuntimeError("Cannot reverse this migration. 'ErvEntry.FanSpeed' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'ErvEntry.FanSpeed'
        db.add_column('hvac-erv', 'FanSpeed',
                      self.gf('django.db.models.fields.CharField')(max_length=8, db_column='fan speed'),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'ErvEntry.Mode'
        raise RuntimeError("Cannot reverse this migration. 'ErvEntry.Mode' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'ErvEntry.Mode'
        db.add_column('hvac-erv', 'Mode',
                      self.gf('django.db.models.fields.CharField')(max_length=14, db_column='mode'),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'ErvEntry.AirDirection'
        raise RuntimeError("Cannot reverse this migration. 'ErvEntry.AirDirection' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'ErvEntry.AirDirection'
        db.add_column('hvac-erv', 'AirDirection',
                      self.gf('django.db.models.fields.CharField')(max_length=16, db_column='air direction'),
                      keep_default=False)

        # Adding unique constraint on 'ErvEntry', fields ['Time', 'Name']
        db.create_unique('hvac-erv', ['time', 'name'])


        # User chose to not deal with backwards NULL issues for 'VrfEntry.Name'
        raise RuntimeError("Cannot reverse this migration. 'VrfEntry.Name' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'VrfEntry.Name'
        db.add_column('hvac-vrf', 'Name',
                      self.gf('django.db.models.fields.CharField')(max_length=32, db_column='name'),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'VrfEntry.FanSpeed'
        raise RuntimeError("Cannot reverse this migration. 'VrfEntry.FanSpeed' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'VrfEntry.FanSpeed'
        db.add_column('hvac-vrf', 'FanSpeed',
                      self.gf('django.db.models.fields.CharField')(max_length=8, db_column='fan speed'),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'VrfEntry.Mode'
        raise RuntimeError("Cannot reverse this migration. 'VrfEntry.Mode' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'VrfEntry.Mode'
        db.add_column('hvac-vrf', 'Mode',
                      self.gf('django.db.models.fields.CharField')(max_length=14, db_column='mode'),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'VrfEntry.AirDirection'
        raise RuntimeError("Cannot reverse this migration. 'VrfEntry.AirDirection' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'VrfEntry.AirDirection'
        db.add_column('hvac-vrf', 'AirDirection',
                      self.gf('django.db.models.fields.CharField')(max_length=16, db_column='air direction'),
                      keep_default=False)

        # Adding unique constraint on 'VrfEntry', fields ['Time', 'Name']
        db.create_unique('hvac-vrf', ['time', 'name'])


    models = {
        u'hvac.erventry': {
            'AirDirectionIndex': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': u"orm['hvac.FanDirections']"}),
            'ErrorSign': ('django.db.models.fields.BooleanField', [], {'db_column': "'error'"}),
            'FanSpeedIndex': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': u"orm['hvac.FanSpeeds']"}),
            'InletTemp': ('django.db.models.fields.FloatField', [], {'db_column': "'measured temp'"}),
            'Meta': {'object_name': 'ErvEntry', 'db_table': "'hvac-erv'"},
            'ModeIndex': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': u"orm['hvac.Modes']"}),
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
            'AirDirectionIndex': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': u"orm['hvac.FanDirections']"}),
            'AutoMax': ('django.db.models.fields.FloatField', [], {'db_column': "'auto max'"}),
            'AutoMin': ('django.db.models.fields.FloatField', [], {'db_column': "'auto min'"}),
            'CoolMax': ('django.db.models.fields.FloatField', [], {'db_column': "'cool max'"}),
            'CoolMin': ('django.db.models.fields.FloatField', [], {'db_column': "'cool min'"}),
            'ErrorSign': ('django.db.models.fields.BooleanField', [], {'db_column': "'error'"}),
            'FanSpeedIndex': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': u"orm['hvac.FanSpeeds']"}),
            'HeatMax': ('django.db.models.fields.FloatField', [], {'db_column': "'heat max'"}),
            'HeatMin': ('django.db.models.fields.FloatField', [], {'db_column': "'heat min'"}),
            'InletTemp': ('django.db.models.fields.FloatField', [], {'db_column': "'measured temp'"}),
            'Meta': {'object_name': 'VrfEntry', 'db_table': "'hvac-vrf'"},
            'ModeIndex': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': u"orm['hvac.Modes']"}),
            'NameIndex': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': u"orm['hvac.Rooms']"}),
            'Running': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'db_column': "'running'", 'blank': 'True'}),
            'SetTemp': ('django.db.models.fields.FloatField', [], {'db_column': "'set temp'"}),
            'Time': ('django.db.models.fields.DateTimeField', [], {'db_column': "'time'"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'temporary': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        }
    }

    complete_apps = ['hvac']