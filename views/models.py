from django.db import models
from django.contrib.contenttypes import generic

from templates.mixins import TemplateMixin

from attrs.mixins import GenericAttrMixin
from entropy.mixins import (
    EnabledMixin, OrderingMixin, TitleMixin, SlugMixin, TextMixin
)

from settings import CONTENT_MODELS


class PageView(models.Model):

    position = models.ForeignKey(
        'positions.Position',
        help_text='The Named Position upon the Page whereas the Page Content View will appear')

    page = models.ForeignKey(
        'pages.Page',
        help_text='The Page to link the Page Content View')

    view = models.ForeignKey(
        'View',
        help_text='The Page Content View to link to the Page')

    class Meta:
        verbose_name = 'Attached page content view'
        verbose_name_plural = 'Attached page content views'


class View(GenericAttrMixin, EnabledMixin, TitleMixin, SlugMixin, TextMixin, TemplateMixin):
    '''
    A View of ViewLinkage or Widgets with a given template.

    Some templates accept parameters, such as slideshow duration
    '''
    class Meta:
        verbose_name = 'Page content view'
        verbose_name_plural = 'Page content views'


class ViewLinkage(EnabledMixin, OrderingMixin):
    '''
    ViewLinkage for View
    '''

    view = models.ForeignKey('View', related_name='linkages')

    content_type = models.ForeignKey(
        'contenttypes.ContentType',
        limit_choices_to={'model__in': CONTENT_MODELS},
        blank=True,
        help_text='Choose the Content Type of the content to link to in the Page Content View',
        null=True
    )
    object_id = models.PositiveIntegerField(
        help_text='Choose the Content Object to link to')
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    class Meta:
        verbose_name = 'Link to content'
        verbose_name_plural = 'Links to content'


    def render(self, context=None):
        '''
        The method would render the html of the content
        '''
        try:
            return self.content_object.render(context)
        except AttributeError:
            # We're choosing to fail silently here
            return ''

