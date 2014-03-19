# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'UserProfile'
        db.create_table(u'accounts_userprofile', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
            ('gender', self.gf('django.db.models.fields.CharField')(default='M', max_length=1)),
        ))
        db.send_create_signal(u'accounts', ['UserProfile'])

        # Adding M2M table for field interests on 'UserProfile'
        m2m_table_name = db.shorten_name(u'accounts_userprofile_interests')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('userprofile', models.ForeignKey(orm[u'accounts.userprofile'], null=False)),
            ('subject', models.ForeignKey(orm[u'courses.subject'], null=False))
        ))
        db.create_unique(m2m_table_name, ['userprofile_id', 'subject_id'])

        # Adding M2M table for field providers on 'UserProfile'
        m2m_table_name = db.shorten_name(u'accounts_userprofile_providers')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('userprofile', models.ForeignKey(orm[u'accounts.userprofile'], null=False)),
            ('provider', models.ForeignKey(orm[u'courses.provider'], null=False))
        ))
        db.create_unique(m2m_table_name, ['userprofile_id', 'provider_id'])

        # Adding M2M table for field enrolled on 'UserProfile'
        m2m_table_name = db.shorten_name(u'accounts_userprofile_enrolled')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('userprofile', models.ForeignKey(orm[u'accounts.userprofile'], null=False)),
            ('course', models.ForeignKey(orm[u'courses.course'], null=False))
        ))
        db.create_unique(m2m_table_name, ['userprofile_id', 'course_id'])

        # Adding M2M table for field completed on 'UserProfile'
        m2m_table_name = db.shorten_name(u'accounts_userprofile_completed')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('userprofile', models.ForeignKey(orm[u'accounts.userprofile'], null=False)),
            ('course', models.ForeignKey(orm[u'courses.course'], null=False))
        ))
        db.create_unique(m2m_table_name, ['userprofile_id', 'course_id'])

        # Adding M2M table for field disliked on 'UserProfile'
        m2m_table_name = db.shorten_name(u'accounts_userprofile_disliked')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('userprofile', models.ForeignKey(orm[u'accounts.userprofile'], null=False)),
            ('course', models.ForeignKey(orm[u'courses.course'], null=False))
        ))
        db.create_unique(m2m_table_name, ['userprofile_id', 'course_id'])


    def backwards(self, orm):
        # Deleting model 'UserProfile'
        db.delete_table(u'accounts_userprofile')

        # Removing M2M table for field interests on 'UserProfile'
        db.delete_table(db.shorten_name(u'accounts_userprofile_interests'))

        # Removing M2M table for field providers on 'UserProfile'
        db.delete_table(db.shorten_name(u'accounts_userprofile_providers'))

        # Removing M2M table for field enrolled on 'UserProfile'
        db.delete_table(db.shorten_name(u'accounts_userprofile_enrolled'))

        # Removing M2M table for field completed on 'UserProfile'
        db.delete_table(db.shorten_name(u'accounts_userprofile_completed'))

        # Removing M2M table for field disliked on 'UserProfile'
        db.delete_table(db.shorten_name(u'accounts_userprofile_disliked'))


    models = {
        u'accounts.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'completed': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'completed_classes'", 'blank': 'True', 'to': u"orm['courses.Course']"}),
            'disliked': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'disliked_classes'", 'blank': 'True', 'to': u"orm['courses.Course']"}),
            'enrolled': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'enrolled_classes'", 'blank': 'True', 'to': u"orm['courses.Course']"}),
            'gender': ('django.db.models.fields.CharField', [], {'default': "'M'", 'max_length': '1'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'interests': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['courses.Subject']", 'symmetrical': 'False', 'blank': 'True'}),
            'providers': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['courses.Provider']", 'symmetrical': 'False', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True'})
        },
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
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

    complete_apps = ['accounts']