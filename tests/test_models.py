#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_django-publica-displays
------------

Tests for `django-publica-displays` models module.
"""

import os
import shutil
import unittest

from displays import models
from displays import factories


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
