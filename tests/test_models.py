#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_django-publica-views
------------

Tests for `django-publica-views` models module.
"""

import unittest

from django.contrib.contenttypes.models import ContentType

from templates.models import Template
from views import models
from views import factories
from views.templatetags.displays_tags import display


class TestDisplays(unittest.TestCase):

    def setUp(self):
        self.display = factories.DisplayFactory(title='Title1',
                                                short_title='Shorty',
                                                enabled=False,
                                                blurb='This is big blurb..')

    def test_title(self):
        self.assertEqual(self.display.title, 'Title1')

    def test_short_title(self):
        self.assertEqual(self.display.short_title, 'Shorty')

    def test_enabled(self):
        self.assertEqual(self.display.enabled, False)

    def test_blurb(self):
        self.assertEqual(self.display.blurb, 'This is big blurb..')

    def tearDown(self):
        pass


class TestDisplayable(unittest.TestCase):
    '''
    A displayable is a made up of one or more displayable which is linked to a display through content type
     _________________________________________________
    |View     |            |  |           |           |
    |         | Viewable|  |  |  Viewable |           |
    |         |            |  |           |           |
    |         |            |  |           |           |
    |          ------------    -----------            |
     -------------------------------------------------
    '''

    def setUp(self):
        self.t1, _ = Template.objects.get_or_create(
            name='templates/test.html', content='detail')
        self.t2, _ = Template.objects.get_or_create(
            name='templates/test_preview.html', content='preview')

        self.display = models.View(title='Title1',
                               short_title='Shorty',
                               enabled=False,
                               blurb='This is big blurb..',
                               slug='home')
        self.display.template = self.t1
        self.display.preview_template = self.t2
        self.display.save()


    def test_display_tag(self):
        self.assertEqual('test', display('home'))


    def test_display_created(self):

        self.t1, _ = Template.objects.get_or_create(
            name='views/default.html', content='')

        self.display = models.View(title='Test2',
                               short_title='Shorty',
                               enabled=True,
                               blurb='This is big blurb..',
                               slug='MainTest')
        self.display.template = self.t1
        self.display.preview_template = self.t1
        self.display.save()

        self.t2, _ = Template.objects.get_or_create(
            name='views/test.html', content='')

        self.t2.save()

        for x in range(10):
            # Create a displayable with some stuff.
            self.displayable = models.Viewable(short_title='short title',
                                                  enabled=True,
                                                  slug='slug'
            )
            self.displayable.template = self.t2
            self.displayable.preview_template = self.t2
            self.displayable.save()
            # Create the linkage between the View and Displayble though content
            self.content = models.ViewLinkage(display=self.display,
                                          content_type=ContentType.objects.get_for_model(self.displayable),
                                          object_id=self.displayable.id)
            self.content.save()

        self.assertTrue('display-MainTest' in display('MainTest'))

    def test_template_rendered(self):
        self.assertTrue('This is a test html template for content displayble' in display('MainTest'))

    def test_template_rendered_count(self):
        self.assertEqual(display('MainTest').count('This is a test html template for content displayble'), 10)


    def tearDown(self):
        pass
        # models.View.objects.all().delete()
