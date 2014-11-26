# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import entropy.mixins


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0001_initial'),
        ('templates', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='View',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.TextField(default=b'', blank=True)),
                ('title', models.CharField(max_length=255)),
                ('short_title', models.CharField(max_length=255, blank=True)),
                ('slug', models.SlugField(max_length=255)),
                ('enabled', models.BooleanField(default=False, db_index=True)),
                ('preview_template', models.ForeignKey(related_name='views_view_preview_templates', blank=True, to='templates.Template', null=True)),
                ('template', models.ForeignKey(related_name='views_view_templates', blank=True, to='templates.Template', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(entropy.mixins.BaseSlugMixin, models.Model),
        ),
        migrations.CreateModel(
            name='ViewLinkage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('enabled', models.BooleanField(default=False, db_index=True)),
                ('order', models.PositiveIntegerField(default=0, blank=True)),
                ('object_id', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(blank=True, to='contenttypes.ContentType', null=True)),
                ('view', models.ForeignKey(related_name='linkages', to='views.View')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
