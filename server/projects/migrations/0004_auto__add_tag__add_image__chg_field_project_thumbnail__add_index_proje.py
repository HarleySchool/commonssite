# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Tag'
        db.create_table(u'projects_tag', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('text', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('hex_color', self.gf('django.db.models.fields.CharField')(max_length=6)),
        ))
        db.send_create_signal(u'projects', ['Tag'])

        # Adding model 'Image'
        db.create_table(u'projects_image', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
        ))
        db.send_create_signal(u'projects', ['Image'])

        # Adding M2M table for field tags on 'Project'
        m2m_table_name = db.shorten_name(u'projects_project_tags')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('project', models.ForeignKey(orm[u'projects.project'], null=False)),
            ('tag', models.ForeignKey(orm[u'projects.tag'], null=False))
        ))
        db.create_unique(m2m_table_name, ['project_id', 'tag_id'])


        # Renaming column for 'Project.thumbnail' to match new field type.
        db.rename_column(u'projects_project', 'thumbnail', 'thumbnail_id')
        # Changing field 'Project.thumbnail'
        db.alter_column(u'projects_project', 'thumbnail_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['projects.Image']))
        # Adding index on 'Project', fields ['thumbnail']
        db.create_index(u'projects_project', ['thumbnail_id'])


    def backwards(self, orm):
        # Removing index on 'Project', fields ['thumbnail']
        db.delete_index(u'projects_project', ['thumbnail_id'])

        # Deleting model 'Tag'
        db.delete_table(u'projects_tag')

        # Deleting model 'Image'
        db.delete_table(u'projects_image')

        # Removing M2M table for field tags on 'Project'
        db.delete_table(db.shorten_name(u'projects_project_tags'))


        # Renaming column for 'Project.thumbnail' to match new field type.
        db.rename_column(u'projects_project', 'thumbnail_id', 'thumbnail')
        # Changing field 'Project.thumbnail'
        db.alter_column(u'projects_project', 'thumbnail', self.gf('django.db.models.fields.CharField')(max_length=128))

    models = {
        u'projects.image': {
            'Meta': {'object_name': 'Image'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'})
        },
        u'projects.project': {
            'Meta': {'object_name': 'Project'},
            'classroom': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'content': ('django.db.models.fields.TextField', [], {}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'students': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['projects.Tag']", 'symmetrical': 'False'}),
            'thumbnail': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['projects.Image']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        u'projects.tag': {
            'Meta': {'object_name': 'Tag'},
            'hex_color': ('django.db.models.fields.CharField', [], {'max_length': '6'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '32'})
        }
    }

    complete_apps = ['projects']