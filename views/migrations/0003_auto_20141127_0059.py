# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('views', '0002_auto_20141126_2109'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='pageview',
            options={'ordering': ('order',), 'verbose_name': 'Attached Page Content View', 'verbose_name_plural': 'Attachable Page Content Views'},
        ),
        migrations.AlterModelOptions(
            name='view',
            options={'verbose_name': 'Page Content View', 'verbose_name_plural': 'Page Content Views that use Content Widgets'},
        ),
        migrations.AlterModelOptions(
            name='viewlinkage',
            options={'verbose_name': 'Link to Content Widget', 'verbose_name_plural': 'Links to Content Widgets'},
        ),
        migrations.AddField(
            model_name='pageview',
            name='order',
            field=models.PositiveIntegerField(default=0, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='view',
            name='preview_template',
            field=models.ForeignKey(related_name='views_view_preview_templates', blank=True, to='templates.Template', help_text=b'Optionally choose a Listing Template that will be used in List Views', null=True, verbose_name=b'Listing/Preview Template'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='view',
            name='template',
            field=models.ForeignKey(related_name='views_view_templates', blank=True, to='templates.Template', help_text=b'Choose a template to render this content', null=True),
            preserve_default=True,
        ),
    ]
