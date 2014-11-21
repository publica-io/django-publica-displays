from django.db import models
from django.contrib.contenttypes import generic

from templates.mixins import TemplateMixin

from attrs.mixins import GenericAttrMixin
from entropy.mixins import (
    EnabledMixin, OrderingMixin, TitleMixin, SlugMixin, TextMixin
)
from images.mixins import ImageMixin

from settings import CONTENT_MODELS


# class ViewInstance(models.Model):
#     '''
#     Views are reuseable
#     '''
#     view = models.ForeignKey('View')
#     channel = models.ForeignKey('channels.Channel')
#     position = models.ForeignKey('positions.Position')
#     links = models.ManyToManyField('menus.Link', blank=True, null=True)

#     def link_ids(self):
#         return self.links.values_list('pk', flat=True)


class View(GenericAttrMixin, EnabledMixin, TitleMixin, SlugMixin, TextMixin, TemplateMixin, ImageMixin):
    """
    A View of ViewLinkage or Widgets with a given template.

    Some templates accept parameters, such as slideshow duration
    """
    pass


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
            # We're choosing to fail silently here
            return ''
