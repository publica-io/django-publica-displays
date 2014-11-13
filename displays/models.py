# -*- coding: utf-8 -*-
from django.db import models

from django.db import models
from django.contrib.contenttypes import generic

from entropy.base import (
    AttributeMixin, EnabledMixin, OrderingMixin, TitleMixin
)

from settings import CONTENT_MODELS


# class DisplayInstance(models.Model):
#     '''
#     Displays are reuseable
#     '''
#
#     display = models.ForeignKey('Display')
#     platform = models.ForeignKey('platforms.Platform')
#     position = models.ForeignKey('positions.Position')
#     links = models.ManyToManyField('menus.Link', blank=True, null=True)
#
#     def link_ids(self):
#         return self.links.values_list('pk', flat=True)


class Display(AttributeMixin, EnabledMixin, TitleMixin):
    '''
    A Display of Content or Widgets with a given template.

    Some templates accept parameters, such as slideshow duration
    '''

    blurb = models.TextField(
        blank=True,
        default='')

    def contents(self):
        '''
        Return the content for this display
        '''
        return [
            content for content in
            self.content_set.enabled().prefetch_related('content_object')
            if content.active
        ]


class Content(EnabledMixin, OrderingMixin):
    '''
    Content for Display
    '''

    display = models.ForeignKey('Display')

    content_type = models.ForeignKey(
        'contenttypes.ContentType',
        limit_choices_to={'model__in': CONTENT_MODELS},
        blank=True,
        null=True
    )
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')
