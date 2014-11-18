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
from views.templatetags.views_tags import view


class TestViews(unittest.TestCase):
    def setUp(self):
        self.view = factories.ViewFactory(title='Title1',
                                          short_title='Shorty',
                                          enabled=False,
                                          blurb='This is big blurb..')

    def test_title(self):
        self.assertEqual(self.view.title, 'Title1')

    def test_short_title(self):
        self.assertEqual(self.view.short_title, 'Shorty')

    def test_enabled(self):
        self.assertEqual(self.view.enabled, False)

    def test_blurb(self):
        self.assertEqual(self.view.blurb, 'This is big blurb..')

    def tearDown(self):
        pass


class TestViewable(unittest.TestCase):
    """
    A viewable is a made up of one or more displayable which is linked to a
    display through content type
     _________________________________________________
    |View     |            |  |           |           |
    |         | Viewable|  |  |  Viewable |           |
    |         |            |  |           |           |
    |         |            |  |           |           |
    |          ------------    -----------            |
     -------------------------------------------------
    """

    def setUp(self):
        self.t1, _ = Template.objects.get_or_create(
            name='templates/test.html', content='test')
        self.t2, _ = Template.objects.get_or_create(
            name='views/test.html', content='preview')

        self.t3, _ = Template.objects.get_or_create(
            name='views/default.html', content='Default')

        self.view1, _ = models.View.objects.get_or_create(title='Title1',
                                                          short_title='Shorty',
                                                          enabled=False,
                                                          blurb='This is big blurb..',
                                                          slug='home',
                                                          template=self.t1,
                                                          preview_template=self.t1)

        self.view2, _ = models.View.objects.get_or_create(title='Test2',
                                                          short_title='Shorty',
                                                          enabled=True,
                                                          blurb='This is big blurb..',
                                                          slug='MainTest',
                                                          template=self.t3,
                                                          preview_template=self.t3
        )

        self.viewable, _ = models.Viewable.objects.get_or_create(short_title='short title',
                                                                 enabled=True,
                                                                 slug='slug',
                                                                 template=self.t2,
                                                                 preview_template=self.t2)

        for x in range(10):
            # Create a displayable with some stuff.

            # Create the linkage between the View and viewable though ViewLinkage
            self.viewlinkage = models.ViewLinkage(view=self.view2,
                                                  content_type=ContentType.objects.get_for_model(self.viewable),
                                                  object_id=self.viewable.id)
            self.viewlinkage.save()


    def test_view_tag(self):
        self.assertEqual('test', view('home'))

    def test_view_created(self):
        self.assertTrue('view-MainTest' in view('MainTest'))

    def test_template_rendered(self):
        self.assertTrue('This is a test html template for content viewable'
                        in view('MainTest'))

    def test_template_rendered_count(self):
        self.assertEqual(view('MainTest').count(
            'This is a test html template for content viewable'), 10)

    def tearDown(self):
        models.ViewLinkage.objects.all().delete()
