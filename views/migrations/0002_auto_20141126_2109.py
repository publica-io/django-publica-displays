# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0002_auto_20141126_1955'),
        ('positions', '0001_initial'),
        ('views', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PageView',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('page', models.ForeignKey(help_text=b'The Page to link the Page Content View', to='pages.Page')),
                ('position', models.ForeignKey(help_text=b'The Named Position upon the Page whereas the Page Content View will appear', to='positions.Position')),
                ('view', models.ForeignKey(help_text=b'The Page Content View to link to the Page', to='views.View')),
            ],
            options={
                'verbose_name': 'Attached page content view',
                'verbose_name_plural': 'Attached page content views',
            },
            bases=(models.Model,),
        ),
        migrations.AlterModelOptions(
            name='view',
            options={'verbose_name': 'Page content view', 'verbose_name_plural': 'Page content views'},
        ),
        migrations.AlterModelOptions(
            name='viewlinkage',
            options={'verbose_name': 'Link to content', 'verbose_name_plural': 'Links to content'},
        ),
        migrations.AlterField(
            model_name='viewlinkage',
            name='content_type',
            field=models.ForeignKey(blank=True, to='contenttypes.ContentType', help_text=b'Choose the Content Type of the content to link to in the Page Content View', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='viewlinkage',
            name='object_id',
            field=models.PositiveIntegerField(help_text=b'Choose the Content Object to link to'),
            preserve_default=True,
        ),
    ]
