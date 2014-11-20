from django.db import models
from django.contrib.contenttypes import generic

from templates.mixins import TemplateMixin

from entropy.mixins import (
    EnabledMixin, OrderingMixin, TitleMixin, SlugMixin, TextMixin
)

from settings import CONTENT_MODELS


# class DisplayInstance(models.Model):
#     '''
#     Displays are reuseable
#     '''
#
#     display = models.ForeignKey('View')
#     platform = models.ForeignKey('platforms.Platform')
#     position = models.ForeignKey('positions.Position')
#     links = models.ManyToManyField('menus.Link', blank=True, null=True)
#
#     def link_ids(self):
#         return self.links.values_list('pk', flat=True)


class View(GenericAttrMixin, EnabledMixin, TitleMixin, SlugMixin, TemplateMixin):
    """
    A View of ViewLinkage or Widgets with a given template.

    Some templates accept parameters, such as slideshow duration
    """

    blurb = models.TextField(blank=True, default='')

    def linked_objects(self):
        '''
        Return the content for this display
        '''
        return [
            content for content in
            self.viewlinkage_set.prefetch_related('content_object')
        ]


class ViewLinkage(EnabledMixin, OrderingMixin):
    """
    ViewLinkage for View
    """

    view = models.ForeignKey('View', related_name='linkages')

    content_type = models.ForeignKey(
        'contenttypes.ContentType',
        limit_choices_to={'model__in': CONTENT_MODELS},
        blank=True,
        null=True
    )
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    def render(self, context=None):
        '''
        The method would render the html of the content
        '''
        try:
            return self.content_object.render(context)
        except AttributeError:
            # Warning we're failing silently here.
            return ''
            # TODO
            # If no render method exists; inspect
            # the object for some fields and try
            # to render a suitable preview.


class Viewable(TemplateMixin, TitleMixin, SlugMixin, TextMixin, EnabledMixin):
    """
    This is a sample test model which defines a content
    type for our display and is used for testing purposes.
    """
    pass
