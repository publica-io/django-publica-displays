from django.db import models
from django.contrib.contenttypes import generic
from django.template import Context
from django.template.loader import get_template

from templates.mixins import TemplateMixin

from entropy.base import (
    AttributeMixin, EnabledMixin, OrderingMixin, TitleMixin, SlugMixin
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


class Display(AttributeMixin, EnabledMixin, TitleMixin, SlugMixin, TemplateMixin):
    '''
    A Display of Content or Widgets with a given template.

    Some templates accept parameters, such as slideshow duration
    '''

    blurb = models.TextField(blank=True, default='')

    def contents(self):
        '''
        Return the content for this display
        '''
        return [
            content for content in
            self.content_set.enabled().prefetch_related('content_object')
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

    def render(self):
        '''
        The method would render the html of the content
        '''
        try:
            return self.content_object.render()
        except AttributeError:
            # Warning we're failing silently here.
            return ''
            # TODO
            # If no render method exists; inspect the object for some fields and try
            # to render a suitable preview.


class Displayable(TemplateMixin, TitleMixin, SlugMixin):
    pass