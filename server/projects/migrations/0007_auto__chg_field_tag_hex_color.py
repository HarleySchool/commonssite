# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Tag.hex_color'
        db.alter_column(u'projects_tag', 'hex_color', self.gf(u'colorful.fields.RGBColorField')())

    def backwards(self, orm):

        # Changing field 'Tag.hex_color'
        db.alter_column(u'projects_tag', 'hex_color', self.gf('django.db.models.fields.CharField')(max_length=6))

    models = {
        u'projects.image': {
            'Meta': {'object_name': 'Image'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'short_name': ('django.db.models.fields.CharField', [], {'max_length': '32'})
        },
        u'projects.project': {
            'Meta': {'object_name': 'Project'},
            'classroom': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'content': ('django.db.models.fields.TextField', [], {}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'images': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'images'", 'symmetrical': 'False', 'to': u"orm['projects.Image']"}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'students': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['projects.Tag']", 'symmetrical': 'False'}),
            'thumbnail': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'thumb'", 'to': u"orm['projects.Image']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        u'projects.tag': {
            'Meta': {'object_name': 'Tag'},
            'hex_color': (u'colorful.fields.RGBColorField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '32'})
        }
    }

    complete_apps = ['projects']