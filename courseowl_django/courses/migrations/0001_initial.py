# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Subject'
        db.create_table(u'courses_subject', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=1000)),
        ))
        db.send_create_signal(u'courses', ['Subject'])

        # Adding model 'Provider'
        db.create_table(u'courses_provider', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=1000)),
        ))
        db.send_create_signal(u'courses', ['Provider'])

        # Adding model 'Source'
        db.create_table(u'courses_source', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=1000)),
        ))
        db.send_create_signal(u'courses', ['Source'])

        # Adding model 'Course'
        db.create_table(u'courses_course', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=1000)),
            ('provider', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['courses.Provider'], null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=3000)),
            ('instructor', self.gf('django.db.models.fields.CharField')(max_length=1000, null=True, blank=True)),
            ('source', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['courses.Source'], null=True, blank=True)),
        ))
        db.send_create_signal(u'courses', ['Course'])

        # Adding M2M table for field subjects on 'Course'
        m2m_table_name = db.shorten_name(u'courses_course_subjects')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('course', models.ForeignKey(orm[u'courses.course'], null=False)),
            ('subject', models.ForeignKey(orm[u'courses.subject'], null=False))
        ))
        db.create_unique(m2m_table_name, ['course_id', 'subject_id'])

        # Adding M2M table for field similarCourses on 'Course'
        m2m_table_name = db.shorten_name(u'courses_course_similarCourses')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_course', models.ForeignKey(orm[u'courses.course'], null=False)),
            ('to_course', models.ForeignKey(orm[u'courses.course'], null=False))
        ))
        db.create_unique(m2m_table_name, ['from_course_id', 'to_course_id'])


    def backwards(self, orm):
        # Deleting model 'Subject'
        db.delete_table(u'courses_subject')

        # Deleting model 'Provider'
        db.delete_table(u'courses_provider')

        # Deleting model 'Source'
        db.delete_table(u'courses_source')

        # Deleting model 'Course'
        db.delete_table(u'courses_course')

        # Removing M2M table for field subjects on 'Course'
        db.delete_table(db.shorten_name(u'courses_course_subjects'))

        # Removing M2M table for field similarCourses on 'Course'
        db.delete_table(db.shorten_name(u'courses_course_similarCourses'))


    models = {
        u'courses.course': {
            'Meta': {'object_name': 'Course'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '3000'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instructor': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            'provider': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['courses.Provider']", 'null': 'True', 'blank': 'True'}),
            'similarCourses': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'similarCourses_rel_+'", 'to': u"orm['courses.Course']"}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['courses.Source']", 'null': 'True', 'blank': 'True'}),
            'subjects': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['courses.Subject']", 'symmetrical': 'False'})
        },
        u'courses.provider': {
            'Meta': {'object_name': 'Provider'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '1000'})
        },
        u'courses.source': {
            'Meta': {'object_name': 'Source'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '1000'})
        },
        u'courses.subject': {
            'Meta': {'object_name': 'Subject'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '1000'})
        }
    }

    complete_apps = ['courses']